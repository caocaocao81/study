from sqlalchemy import Table, MetaData, func
import myproduct.venv.Model as Data
from myproduct.venv.main import db
import time


class Suggestion(db.Model):
    __table__ = Table('user_suggestion', MetaData(bind=db.engine), autoload=True)

    def get_all_suggestion(self):
        s = Suggestion()
        result = db.session.query(Suggestion).filter().all()
        result = s.change_data(result)
        db.session.close()
        return result

    def upate_like_count(self,l):  # 更新用户点赞数
        __like = [{'id': k, 's_like': l[k]} for k in l]
        try:
            db.session.bulk_update_mappings(Suggestion, __like)
            db.session.commit()
        except:
            db.session.rollback()  # 事务回滚
        db.session.close()

    def insert_sug_by_uname(self,uname,title,sug):  # 插入用户建议
        Sug = Suggestion(time=time.time(),username=uname,
                         title=title,suggestion=sug)
        try:
            db.session.add(Sug)
            db.session.commit()
        except:
            db.session.rollback()
        db.session.close()

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
#     # suggest =Suggestion()
#     # result = suggest.get_all_suggestion()
#     # print(result)
#     l = {'1': '1', '2': '1', '3': '1'}
#     like = [{'id':k,'s_like':l[k]} for k in l]
#     print(like)
#     # db.session.bulk_update_mappings(Suggestion,like)
#     # db.session.commit()