from myproduct.venv.Model.videotime import VideoTime


# 通过课程编号和用户编号得到上一次观看时间
def select_video_time_by_id(uid,cid):
    vd = VideoTime()
    time = vd.select_video_time_by_id(uid,cid)
    return time



# if __name__ == '__main__':
#
#     print(select_video_time_by_id('23','1'))
