from myproduct.venv.Model.user import User
import hashlib
from flask import Blueprint


# 获取用户所有数据
def user_select_by_name(name):
    users = User()
    row = users.select_user_by_name(name)
    list = users.change_data(row)
    return list

# 用户登录判断
def validate(username,pwd1):
    return User().validate(username,pwd1)

# 获取用户编号
def user_select_uid_by_name(name):
    users = User()
    row = users.select_user_by_name(name)
    list = users.change_data(row)
    try:
        uid = list[0]['uid']
    except:
        return 'error'
    else:
        return uid


# 用户注册
def user_insert(name,pwd,pwd1,email,phone):
    users = User()
    md5 = hashlib.md5()
    if pwd != pwd1:
        return "两次密码不一致"
    # 加密密码
    md5.update(pwd.encode('utf-8'))
    pwd_md5 = md5.hexdigest()
    try:  # 添加用户
        users.insert_user(name,pwd_md5,email,phone)
    except:
        return "注册失败请重试"
    else:
        return "注册成功"


def user_delete(name):
    users = User()
    try:
        users.delete_user_by_name(name)
    except:
        return "删除失败请重试"
    else:
        return "删除成功"


def user_login(name,pwd):  # 验证用户登录
    users = User()
    # 加密密码
    md5 = hashlib.md5()  # 设置在函数中防止多次加密和数据库中密码不一致
    md5.update(pwd.encode('utf-8'))
    pwd_md5 = md5.hexdigest()
    a = users.check_name_pwd(name,pwd_md5)
    return a
