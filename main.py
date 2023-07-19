import os
import string
from ttkbootstrap import *
from tkinter import Text, Button
from pickle import load, dump
from threading import Thread
from time import sleep

PATH_DATA = os.path.join(os.path.dirname(__file__), "data")
PATH_USERS = os.path.join(PATH_DATA, "users.fishc")

(
    CODE_SUCCESS,
    CODE_NOT_FOUND,
    CODE_DUPLICATE,
    CODE_WRONG_PARAMETER,
    CODE_LENGTH_ERROR,
    CODE_WEAK_PASSWORD
) = range(6)

SAFE_LOWEST, SAFE_1, SAFE_2, SAFE_3, SAFE_HIGHEST = range(5)

def check_dir(path):
    """
    检查一个目录是否存在，如果不存在就创建一个
    :param path: 路径
    :return: None
    """
    if not os.path.isdir(path):
        os.mkdir(path)

def check_file(path, binary=False, default=""):
    """
    检查一个文件是否存在，如果不存在就创建一个
    :param path: 路径
    :param binary: 是否为二进制文件
    :param default: 如果此文件为空，默认值
    :return: none
    """
    if not os.path.isfile(path):
        if binary:
            with open(path, "wb") as f:
                dump(default, f)
        else:
            with open(path, "w") as f:
                f.write(default)

check_dir(PATH_DATA)
check_file(PATH_USERS, True, [])

class User:
    def __init__(self, username, password):
        """
        创建一个用户
        :param username: 用户名
        :param password: 密码
        """
        self.username = username
        self.password = password
    
    def info(self):
        """
        获取某人的 info
        :return: info `(username, password)`
        """
        return self.username, self.password

def add_user(username, password):
    """
    将一个用户添加到 `data/users.fishc`
    :param username: 用户名
    :param password: 密码
    :return: 被添加的用户
    """
    user = User(username, password)
    data = get_userlist()
    data.append(user)
    write_into_userlist(data)
    return user

def remove_user(username, password):
    """
    从用户列表移除一个用户（data/users.fishc）
    :param username: 用户名
    :param password: 密码
    :return: 被删除的用户
    """
    data = get_userlist()
    index = None
    for i, (user, pwd) in enumerate(map(User.info, data)):
        if user == username:
            if pwd == password:
                index = i
                break
            else:
                raise ValueError("wrong password")
    else:
        raise ValueError("wrong username")
    data.pop(index)
    write_into_userlist(data)

def get_userlist():
    """
    获取用户列表（data/users.fishc）
    :return: 用户列表 [User(username, password), ...]
    """
    with open(PATH_USERS, "rb") as f:
        data = load(f)
    return data

def write_into_userlist(data):
    """
    将内容写入用户列表（data/users.fishc）
    :param data: 新内容
    :return: None
    """
    with open(PATH_USERS, "wb") as f:
        dump(data, f)

def login(username, password):
    """
    登录进一个账号
    :param username: 用户名
    :param password: 密码
    :return: (状态码, 找到的用户)
    """
    users = get_userlist()
    # 为了便于判断，用 for 循环
    for user in users:
        if user.info() == (username, password):
            # 登录成功
            return (CODE_SUCCESS, user)
    return (CODE_NOT_FOUND, None)

def register(username, password):
    """
    注册一个用户
    :param username: 用户名
    :param password: 密码
    :return: (状态码, 新用户)
    """
    # 检查用户名是否已被使用
    users = [user.username for user in get_userlist()]
    if username in users:
        return (CODE_DUPLICATE, None)
    if username == "Admin":
        return (CODE_SUCCESS, add_user(username, password))
    if not 3 <= len(username) < 11:
        return (CODE_LENGTH_ERROR, None)
    # 密码强度
    password_strength = check_password_strength(password)
    # 必须达到 SAFE_3 级别
    if password_strength < SAFE_3:
        if password_strength == SAFE_LOWEST:
            show_message(label_password_weak0)
        elif password_strength == SAFE_1:
            show_message(label_password_weak1)
        elif password_strength == SAFE_2:
            show_message(label_password_weak2)
        return (CODE_WEAK_PASSWORD, None)
        
    # 创建用户
    return (CODE_SUCCESS, add_user(username, password))

def command_login():
    """
    作为 button 的 `command` 属性的函数，用于调用 `login()`
    :return: None
    """
    value_username = entry_username.get()
    value_password = entry_password.get()
    status = login(value_username, value_password)[0]
    if status == CODE_SUCCESS:
        show_message(label_message2)
        frame_login.place_forget()
    else:
        show_message(label_message1)

def command_register():
    """
    作为 button 的 `command` 属性的函数，用于调用 `register()`
    :return: None
    """
    value_username = entry_username.get()
    value_password = entry_password.get()
    status = register(value_username, value_password)[0]
    if status == CODE_SUCCESS:
        show_message(label_message3)
    elif status == CODE_DUPLICATE:
        show_message(label_message4)
    elif status == CODE_LENGTH_ERROR:
        show_message(label_message5)

def disappear(obj, method, time1, time2):
    """
    使某个控件在几秒后消失。（打字机特效，指定秒数少一个字符）

    注意，请使用 `threading.Thread` 调用此函数，否则会造成窗口卡死。
    :param obj: 控件
    :param method: 控件使用的方法，为“place”、“pack”、“grid”中的一种
    :param time1: 过多久才开始消失
    :param time2: 消失的时间，多久消失一个字
    :return: 状态码
    """
    # 先提前搞到文字，到时候消失了要放回去
    text = obj["text"]
    # 等待
    sleep(time1)
    while obj["text"]:
        # 减少一个字
        obj["text"] = obj["text"][:-1]
        sleep(time2)
    obj["text"] = text
    # 使控件消失
    getattr(obj, f"{method}_forget")()

def show_message(obj):
    """
    显示一条消息
    :param obj: 消息对象（`Label`）
    :return: None
    """
    obj.place(**temp3)
    Thread(target=disappear, args=(obj, "place", 1, 0.1)).start()

def check_password_strength(pwd):
    """
    检查密码的安全级别。规则如下：

    |             判断条件         | 判断结果 |    返回值      |
    |:-----------------------------|:---------|:---------------|
    | 密码长度 < 10                | 不安全   | `SAFE_LOWEST`  |
    | 密码只含有数字               | 不太安全 | `SAFE_1`       |
    | 密码只有字母                 | 中等     | `SAFE_2`       |
    | 密码有字母和数字             | 有点安全 | `SAFE_3`       |
    | 密码有数字、大小写字母和符号 | 安全     | `SAFE_HIGHEST` |

    :param pwd: 密码
    :return: 参考表格
    """
    if len(pwd) < 10:
        return SAFE_LOWEST
    number = False
    lowercase = False
    uppercase = False
    punctuation = False
    for char in pwd:
        # 避免二次判断
        if not number and char in string.digits:
            number = True
        if not lowercase and char in string.ascii_lowercase:
            lowercase = True
        if not uppercase and char in string.ascii_uppercase:
            uppercase = True
        if not punctuation and char in string.punctuation:
            punctuation = True
    result = (number, lowercase, uppercase, punctuation)
    result_count = result.count(True)
    if number and result_count == 1:
        # 只有数字
        return SAFE_1
    if (lowercase or uppercase) and 1 <= result_count < 3:
        # 只有字母
        return SAFE_2
    if (lowercase or uppercase) and number and 2 <= result_count < 4:
        # 大/小写字母且有数字
        return SAFE_3
    if lowercase and uppercase and number and punctuation:
        return SAFE_HIGHEST

def change_password_visiblity():
    """
    切换密码输入框的可见性，如果密码没隐藏则隐藏，如果隐藏了就不隐藏
    :return: None
    """
    if entry_password["show"] == "":
        # 密码没有隐藏
        entry_password["show"] = "*"
        button_change_password_visiblity["text"] = "显示密码"
    else:
        # 密码隐藏了
        entry_password["show"] = ""
        button_change_password_visiblity["text"] = "隐藏密码"

def change_admin_tool_visiblity():
    """
    切换 Admin Tool 的可见性
    :return: None
    """
    if bool(frame_admin_tool.winfo_manager()):
        frame_admin_tool.place_forget()
        # 没隐藏
        button_admin_tool["text"] = "打开 Admin Tool"
    else:
        frame_admin_tool.place(relx=0.9, rely=0.2, anchor="ne")
        # 隐藏了
        button_admin_tool["text"] = "关闭 Admin Tool"

def change_users_visiblity():
    """
    管理用户（Admin Tool）
    :return: None
    """
    # 以防万一
    text_users.delete(0.0, END)
    if bool(text_users.winfo_manager()):
        button_show_userlist["text"] = "显示用户列表"
        text_users.grid_forget()
    else:
        button_show_userlist["text"] = "隐藏用户列表"
        text_users.grid(row=1, column=0, **temp2)
        text_users.insert(END, '\n'.join([' '.join(user.info()) for user in get_userlist()]))

temp1 = {"padx": 10, "pady": 10}
temp2 = {"padx": 5, "pady": 5}
temp3 = {"relx": 0.8, "rely": 0.2, "anchor": "ne"}

bootstyle = {
    "primary":   {"fg": "white", "bg": "#4582ec"},
    "secondary": {"fg": "white", "bg": "#adb5db"},
    "success":   {"fg": "white", "bg": "#02b875"},
    "info":      {"fg": "white", "bg": "#17a2b8"},
    "warning":   {"fg": "white", "bg": "#f0ad4e"},
    "danger":    {"fg": "white", "bg": "#d9534f"},
    "light":     {"fg": "black", "bg": "#f8f9fa"},
    "dark":      {"fg": "white", "bg": "#343a40"}
}

root = Window("This Forum 1.0 Beta 测试版本 - By dddddgz", "morph")
root.geometry("1000x800+100+100")

label_message1 = Label(root, bootstyle="danger", text="密码或用户名错误")
label_message2 = Label(root, bootstyle="success", text="登录成功！")
label_message3 = Label(root, bootstyle="success", text="注册成功！")
label_message4 = Label(root, bootstyle="danger", text="用户名已存在")
label_message5 = Label(root, bootstyle="danger", text="用户名字符数限制：3-10")

label_password_weak0 = Label(root, bootstyle="danger", text="密码太弱，没有达到10个字符")
label_password_weak1 = Label(root, bootstyle="danger", text="密码只有数字")
label_password_weak2 = Label(root, bootstyle="danger", text="密码只有大写或小写字母")

frame_login = Frame(root)

label_username = Label(frame_login, bootstyle="dark", text="用户名")
label_username.grid(row=0, column=0, **temp1, columnspan=2)
entry_username = Entry(frame_login, bootstyle="info", width=30)
entry_username.grid(row=1, column=0, **temp1, columnspan=2)

label_password = Label(frame_login, bootstyle="dark", text="密码")
label_password.grid(row=2, column=0, **temp1, columnspan=2)
entry_password = Entry(frame_login, bootstyle="primary", width=30)
entry_password.grid(row=3, column=0, **temp1, columnspan=2)

button_change_password_visiblity = Button(frame_login, **bootstyle["primary"])
button_change_password_visiblity["command"] = change_password_visiblity
button_change_password_visiblity.grid(row=3, column=2, **temp1)
change_password_visiblity()

button_login = Button(frame_login)
button_login["text"] = "登录"
button_login["width"] = 8
button_login["command"] = command_login
button_login.grid(row=4, column=0, **temp1)

button_register = Button(frame_login)
button_register["text"] = "注册"
button_register["width"] = 8
button_register["command"] = command_register
button_register.grid(row=4, column=1, **temp1)

frame_login.place(relx=0.5, rely=0.5, anchor="center")

button_admin_tool = Button(root, **bootstyle["info"])
button_admin_tool["text"] = "打开 Admin Tool"
button_admin_tool["command"] = change_admin_tool_visiblity
button_admin_tool.place(relx=0.8, rely=0.9, anchor="ne")

frame_admin_tool = Frame(root)

button_show_userlist = Button(frame_admin_tool, **bootstyle["warning"])
button_show_userlist["text"] = "查看用户列表"
button_show_userlist["command"] = change_users_visiblity
button_show_userlist.grid(row=0, column=0, **temp2)

text_users = Text(frame_admin_tool, width=10, height=10)

root.mainloop()
