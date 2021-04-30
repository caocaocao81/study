from sqlalchemy import Table, MetaData, func
from myproduct.venv.Model.data import User
from myproduct.venv.Model.data import Course
from myproduct.venv.main import db


class VideoTime(db.Model):
    __table__ = Table('videotime', MetaData(bind=db.engine), autoload=True)

    def select_video_time_by_id(self,uid,cid):
        result = db.session.query(VideoTime).filter(
            Course.cid==cid,User.uid==uid).all()
        # 获得相应时间
        result1 = VideoTime.change_data(self,result)
        time = result1[0]['time']
        db.session.close()
        return time

    def change_data(self,row):
        # 单表查询提取数据
        list = []
        for r in row:
            dict = {}
            for k, v in r.__dict__.items():
                if not k.startswith('_sa_instance_state'):
                    dict[k] = v
            list.append(dict)
        return list

    def change_data_more(self,result):
        # 多表查询提取数据
        list = []
        for r in result:
            for j in r:
                dict = {}
                for k, v in j.__dict__.items():
                    if not k.startswith('_sa_instance_state'):
                        dict[k] = v
                list.append(dict)
        return list


# if __name__ == '__main__':
#     vd = VideoTime()
#
#     result = vd.select_video_time_by_id('23','1')
#     # result = vd.change_data(result)
#
#     print(result)