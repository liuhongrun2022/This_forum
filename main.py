import os
from pickle import load, dump

PATH_DATA = os.path.join(os.path.dirname(__file__), "data")
PATH_USERS = os.path.join(PATH_DATA, "users.fishc")

def check_dir(path):
    """
    check a directory if it exists
    if it does not exist, make one
    :param path: directory path
    :return: none
    """
    if not os.path.isdir(path):
        os.mkdir(path)

def check_file(path, binary=False, default=""):
    """
    check a file if it exists (if it does not exist, create one)
    :param path: filepath
    :param binary: is this file a binary file (default=false)
    :param default: if this file does not exist, file content (default="")
    :return: none
    """
    if not os.path.isfile(path):
        if binary:
            with open(path, "wb") as f:
                dump(default, f)
        else:
            with open(path, "w") as f:
                f.write(default)

class User:
    def __init__(self, username, password):
        """
        create one user (use user-defined class can make problem easier)
        :param username: username
        :param password: password
        """
        self.username = username
        self.password = password
    
    def info(self):
        """
        get someone's info
        :return: info: (username, password)
        """
        return self.username, self.password

def add_user(username, password):
    """
    add one user to data/users.fishc
    :param username: username of new user
    :param password: password of new user
    :return: user that is added
    """
    user = User(username, password)
    data = get_userlist()
    data.append(user)
    write_into_userlist(data)
    return user

def remove_user(username, password):
    """
    remove one user from userlist (data/users.fishc)
    :param username: username of new user
    :param password: password of new user
    :return: user that is removed
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
    get userlist (data/users.fishc)
    :return: userlist
    """
    with open(PATH_USERS, "rb") as f:
        data = load(f)
    return data

def write_into_userlist(data):
    """
    write into userlist (data/users.fishc)
    :param data: target data
    :return: new userlist
    """
    with open(PATH_USERS, "wb") as f:
        dump(data)
