import os
from ttkbootstrap import *
from pickle import load, dump

PATH_DATA = os.path.join(os.path.dirname(__file__), "data")
PATH_USERS = os.path.join(PATH_DATA, "users.fishc")

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

def get_user_infolist():
    """
    获取所有用户的 info
    :return: info [(username, password), ...]
    """
    return [user.info() for user in get_userlist()]

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
    登录进一个账号（如果找不到用户，元组第二项会返回 `None`）
    :param username: 用户名
    :param password: 密码
    :return: (状态码, 找到的用户)
    """
    users = get_user_infolist()
    if (username, password) in users:
        print("成功登录！")

def register(username, password):
    """
    注册一个用户
    :param username: 用户名
    :param password: 密码
    :return: (状态码, 新用户)
    """
    # 检查用户名是否已被使用
    users = get_user_infolist()
    if username in users:
        print("用户名已被使用")
        return
    # 创建用户
    return add_user(username, password)

def command_login():
    """
    作为 button 的 `command` 属性的函数，用于调用 `login()`
    :return: None
    """
    value_username = entry_username.get()
    value_password = entry_password.get()
    login(value_username, value_password)

def command_register():
    """
    作为 button 的 `command` 属性的函数，用于调用 `register()`
    :return: None
    """
    value_username = entry_username.get()
    value_password = entry_password.get()
    register(value_username, value_password)

option = {"padx": 30, "pady": 10}
root = Window("This Forum 1.0 Beta", "morph")
root.geometry("1800x1000+50+50")
label_username = Label(root, bootstyle="dark", text="用户名")
label_username.grid(row=0, column=0, **option, columnspan=2)
entry_username = Entry(root, bootstyle="info", width=30)
entry_username.grid(row=1, column=0, **option, columnspan=2)
label_password = Label(root, bootstyle="dark", text="密码")
label_password.grid(row=2, column=0, **option, columnspan=2)
entry_password = Entry(root, bootstyle="primary", width=30, show="*")
entry_password.grid(row=3, column=0, **option, columnspan=2)
button_login = Button(root, bootstyle="success", text="登录", width=8)
button_login["command"] = command_login
button_login.grid(row=4, column=0, **option)
button_register = Button(root, bootstyle="info", text="注册", width=8)
button_register["command"] = command_register
button_register.grid(row=4, column=1, **option)
root.mainloop()
