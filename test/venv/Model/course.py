from sqlalchemy import Table, MetaData, func
from myproduct.venv.main import db
import json

class Course(db.Model):
    __table__ = Table('course', MetaData(bind=db.engine), autoload=True)

    def select_course_by_name(self,cname):  # 根据姓名进行查找（返回一个列表）
        # row = db.session.query(User).filter(User.name == name).all()  # 获得一个列表
        result = db.session.query(Course).filter(Course.cname == cname).all()
        db.session.close()
        return result

    def select_course_by_name_like(self,cname):  # 根据姓名模糊查找
        result = db.session.query(Course).filter(Course.cname.like('%' + cname + '%')).all()
        db.session.close()
        return result

    def select_course_all(self):
        result = db.session.query(Course).filter().all()
        db.session.close()
        return result

    def change_data(self,row):  # 将列表分离（功能模糊，需要自调。不推荐使用）
        list = []
        for r in row:
            dict = {}
            for k, v in r.__dict__.items():
                if not k.startswith('_sa_instance_state'):
                    dict[k] = v
            list.append(dict)
        return list


# if __name__ == '__main__':
#     course = Course()
#     result = course.select_course_all()
#     result1 = course.change_data(result)
#     print(result1)
#     result_json = json.dumps(result1,ensure_ascii=False)
#     print(result_json)
#     print(result[1].cname)