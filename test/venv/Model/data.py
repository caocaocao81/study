from sqlalchemy import Table, MetaData, func
from myproduct.venv.main import db

# 会员数据模型
class User(db.Model):
    __table__ = Table('user', MetaData(bind=db.engine), autoload=True)


# 视频播放时间
class VideoTime(db.Model):
    __table__ = Table('videotime', MetaData(bind=db.engine), autoload=True)


# 课程
class Course(db.Model):
    __table__ = Table('course', MetaData(bind=db.engine), autoload=True)


# 操作数据
class Data(db.Model):
    __table__ = Table('data', MetaData(bind=db.engine), autoload=True)

class Mail(db.Model):
    __table__ = Table('mail',MetaData(bind=db.engine),autoload=True)
