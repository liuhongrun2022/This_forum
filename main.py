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
    :return: 用户列表
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
        dump(data)

root = Window("This Forum 1.0 Beta", "superhero")
root.geometry("1800x1000+50+50")
username = Entry(root, bootstyle="primary", width=50)
username.grid(row=0, column=0, padx=20, pady=20)
root.mainloop()
