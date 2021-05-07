
from myproduct.venv.Redis import *
from redis import WatchError
from concurrent.futures import ProcessPoolExecutor

# 减库存函数, 循环直到减库存完成
# 库存充足, 减库存成功, 返回True
# 库存不足, 减库存失败, 返回False
def decr_stock(pid,name):
    product_name = 'product_' + str(pid) + '_kc'
    product_set = 'product_'+str(pid)+'_set'
    with redis_conn.pipeline() as pipe:
        while True:
            try:
                pipe.watch(product_name)
                count = int(pipe.get(product_name))
                if count > 0:  # 有库存
                    # 事务开始
                    pipe.multi()  # 将命令放到队伍中
                    pipe.decr(product_name)
                    if redis_conn.sismember(product_set,name) == 1:
                        return 1
                    pipe.sadd(product_set,name)
                    # execute返回命令执行结果列表,这里只有一个decr返回当前值
                    print(pipe.execute()[0])
                    return 2
                else:
                    return 3
            except WatchError as ex:
                print(ex)
                pipe.unwatch()


def worker(pid,name):
    while True:
        # 没有库存就退出
        a = decr_stock(pid,name)
        if a == 3:
            return '当前没有库存'
            # break
        elif a == 1:
            return '该商品只能购买一次哦！'
        else:
            return '购买成功'