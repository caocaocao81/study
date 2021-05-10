from myproduct.venv.Redis import *
import time

class Rlike():
    sug_set = redis_conn_slave.smembers('sug_set')

    def get_count(self,sug_id):  # 获得点赞数
        __count = 'sug_user_like_set_'+str(sug_id)
        return redis_conn_slave.scard(__count)

    def change_count(self,sug_all):  # 更新点赞数
        for i in sug_all:
            i['s_like'] = self.get_count(i['id'])
        return sug_all

    def dis_like_user(self,sug_id,uname):
        __sug_count = str(sug_id)
        __sug_user_like = 'sug_user_like_set_' + str(sug_id)
        __sug_user_like_sug_name = 'sug_user_like_'+str(sug_id) + '_' + uname
        if redis_conn.srem(__sug_user_like,uname):
            redis_conn.sadd('sug_set',sug_id)
            redis_conn.hset(__sug_user_like_sug_name,'like_state',0)
            redis_conn.hincrby('sug_count',__sug_count,-1)
            return '取消点赞成功'
        else:
            return '取消点赞失败'

    def like_user(self,sug_id,uname):
        __sug_count = str(sug_id)
        __sug_user_like = 'sug_user_like_set_' + str(sug_id)
        __sug_user_like_sug_name = 'sug_user_like_' + str(sug_id) + '_' + uname
        like_time = time.strftime("%Y-%m-%d-%H:%M", time.localtime())
        if redis_conn.sadd(__sug_user_like,uname):
            redis_conn.hmset(__sug_user_like_sug_name, {'like_state':1,'time':like_time})
            redis_conn.sadd('sug_set', sug_id)
            redis_conn.hincrby('sug_count',__sug_count)
            return '点赞成功'
        else:
            return '点赞失败'

    # def insert_mysql(self):  # 定时更新点赞数  协程进行(再开一个进程有点浪费资源)
    #     while True:
    #         await asyncio.sleep(600)
    #         id_like = redis_conn.hgetall('sug_count')
    #         sug = Suggestion()
    #         sug.upate_like_count(id_like)

    def if_like(self,sug,uname):
        like = {}
        for i in sug:
            __sug = 'sug_user_like_set_' + str(i['id'])
            if uname in redis_conn_slave.smembers(__sug):
                like[i['id']] = 1
            else:
                like[i['id']] = 0
        return like


# if __name__ == '__main__':
#     a = redis_conn.hgetall('sug_count')
#     print(a)



