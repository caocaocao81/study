from flask import session
from sqlalchemy import Table, MetaData, func
from myproduct.venv.main import db
import hashlib


# 用户登录和注册返回的提示信息
def validate(username,pwd1):
    user = db.session.query(User).filter(User.name == username).first()
    md5 = hashlib.md5()
    if user:
        # 加密密码
        md5.update(pwd1.encode('utf-8'))
        pwd_md5 = md5.hexdigest()
        if user.pwd == pwd_md5:
            return "登陆成功"
        else:
            return "密码错误"
    else:
        return "用户名不存在"


class User(db.Model):
    __table__ = Table('user', MetaData(bind=db.engine), autoload=True)

    def select_user_by_name(self,name):
        # row = db.session.query(User).filter(User.name == name).all()  # 获得一个列表
        row = db.session.query(User).filter(User.name == name).all()
        db.session.close()
        return row

    def select_user_note(self,name):  # 获得用户笔记
        row = db.session.query(User).filter(User.name == name).first()
        db.session.close()
        return row.note

    def insert_user(self,name,pwd,email,phone):
        insert = User(name=name,pwd=pwd,power='lower',email=email,phone=phone,note='')
        db.session.add(insert)
        db.session.commit()
        db.session.close()

    def delete_user_by_name(self,name):  # 根据用户名删除用户
        delete = db.session.query(User).filter(User.name == name).first()  # 用all()的话因为是列表所以会报错
        try:
            db.session.delete(delete)
            db.session.commit()
        except:
            db.session.rollback()
        db.session.close()

    def select_user_by_name_like(self,name):  # 根据姓名模糊查找
        select_like = db.session.query(User).filter(User.name.like('%'+name+'%')).first()
        db.session.close()
        return select_like

    def updata_user(self,email,phone,pwd):  # 更新用户信息
        try:
            db.session.add(User(email=email,phone=phone,pwd=pwd))
            db.session.commit()
        except:
            db.session.rollback()
        db.session.close()

    def check_name_pwd(self,name,pwd):

        a = db.session.query(User).filter(User.name == name,User.pwd == pwd).first()
        db.session.close()
        return a

    # 用户登录和注册返回的提示信息
    def validate(self,username, pwd1,vcode):
        user = db.session.query(User).filter(User.name == username).first()
        md5 = hashlib.md5()
        try:
            if vcode == session['vcode']:
                if user:
                    # 加密密码
                    md5.update(pwd1.encode('utf-8'))
                    pwd_md5 = md5.hexdigest()
                    if user.pwd == pwd_md5:
                        return '登陆成功'
                    else:
                        return '密码错误'
                else:
                    return '用户名不存在'
            else:
                return '验证码错误'
        except:
            return '未知错误'

    def change_data(self,row):
        list = []
        for r in row:
            dict = {}
            for k, v in r.__dict__.items():
                if not k.startswith('_sa_instance_state'):
                    dict[k] = v
            list.append(dict)
        return list


# if __name__ == '__main__':
#     use = User()
#     a = use.select_user_note('452')
#     print(a)