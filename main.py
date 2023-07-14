import os
from ttkbootstrap import *
from pickle import load, dump
from threading import Thread
from time import sleep

PATH_DATA = os.path.join(os.path.dirname(__file__), "data")
PATH_USERS = os.path.join(PATH_DATA, "users.fishc")

CODE_SUCCESS, CODE_NOT_FOUND, CODE_DUPLICATE = range(0, 3)
CODE_WRONG_PARAMETER, CODE_LENGTH_ERROR = range(3, 5)

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
    if not 3 < len(username) < 10:
        return (CODE_LENGTH_ERROR, None)
    if username in users:
        return (CODE_DUPLICATE, None)
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
    `"""
    obj.place(**grid_option2)
    Thread(target=disappear, args=(obj, "place", 1, 0.1)).start()

grid_option1 = {"padx": 30, "pady": 10}
grid_option2 = {"relx": 0.8, "rely": 0.2, "anchor": "ne"}

root = Window("This Forum 1.0 Beta 测试版本 - By dddddgz and liu2023", "morph")
root.geometry("800x800+50+50")

label_message1 = Label(root, bootstyle="danger", text="密码或用户名错误")
label_message2 = Label(root, bootstyle="success", text="登录成功！")
label_message3 = Label(root, bootstyle="success", text="注册成功！")
label_message4 = Label(root, bootstyle="danger", text="用户名已存在")
label_message5 = Label(root, bootstyle="danger", text="用户名字符数限制：3-10")

frame_login = Frame(root)
label_username = Label(frame_login, bootstyle="dark", text="用户名")
label_username.grid(row=0, column=0, **grid_option1, columnspan=2)
entry_username = Entry(frame_login, bootstyle="info", width=30)
entry_username.grid(row=1, column=0, **grid_option1, columnspan=2)
label_password = Label(frame_login, bootstyle="dark", text="密码")
label_password.grid(row=2, column=0, **grid_option1, columnspan=2)
entry_password = Entry(frame_login, bootstyle="primary", width=30, show="*")
entry_password.grid(row=3, column=0, **grid_option1, columnspan=2)
button_login = Button(frame_login, text="登录", width=8)
button_login["command"] = command_login
button_login.grid(row=4, column=0, **grid_option1)
button_register = Button(frame_login, text="注册", width=8)
button_register["command"] = command_register
button_register.grid(row=4, column=1, **grid_option1)
frame_login.place(relx=0.5, rely=0.5, anchor='center')

root.mainloop()
