import redis
import asyncio
from myproduct.venv.Model.suggestion import *

__redis_pool = redis.ConnectionPool(host='121.43.147.188', port=337,
                                    password='cao123.', db=1, decode_responses=True)  # decode_responses转换编码

redis_conn = redis.Redis(connection_pool=__redis_pool)


async def __insert_mysql():  # 定时更新点赞数  协程进行(再开一个进程有点浪费资源)
    while True:
        # await asyncio.sleep(600)
        id_like = redis_conn.hgetall('sug_count')
        print(id_like)
        sug = Suggestion()
        sug.upate_like_count(id_like)
        print('111')
        await asyncio.sleep(600)


def run_insert():
    asyncio.run(__insert_mysql())


if __name__ == '__main__':
    run_insert()
