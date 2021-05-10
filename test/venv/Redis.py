import threading
import redis
from myproduct.venv.Model.suggestion import *
from myproduct.venv.Model.product import *

__redis_pool = redis.ConnectionPool(host='', port=337,
                                    password='.', db=1,
                                    decode_responses=True, max_connections=100)  # decode_responses转换编码

redis_conn = redis.Redis(connection_pool=__redis_pool)

__redis_pool_slave = redis.ConnectionPool(host='121.43.147.188', port=338,
                                          password='cao123.', db=1,
                                          decode_responses=True, max_connections=100)  # decode_responses转换编码

redis_conn_slave = redis.Redis(connection_pool=__redis_pool_slave)


class get_all_kc():  # 初始化将mysql库存导入redis
    def get_all(self):
        pro = Product()
        result = pro.select_all_product()
        products = {k['pid']: k['Inventory'] for k in result}
        redis_conn.hmset('products_hash', products)



class insert_mysql():
    def __insert_mysql(self):  # 定时更新点赞数  协程进行(再开一个进程有点浪费资源)
        while True:
            id_like = redis_conn_slave.hgetall('sug_count')
            sug = Suggestion()
            sug.upate_like_count(id_like)
            # 获得product真实库存
            product_kc = redis_conn_slave.hgetall('products_hash')
            pro = Product()
            pro.update_product_Inventory(product_kc)
            time.sleep(600)

    def start_new_thread(self):
        thread = threading.Thread(target=self.__insert_mysql, args=())
        thread.setDaemon(True)
        thread.start()


if __name__ == '__main__':
    # pro = Product()
    # result = pro.select_all_product()
    # products = {k['pid']: k['Inventory'] for k in result}
    # print(products)
    # p = redis_conn_slave.hget('products_hash',1)
    # print(type(p))
    # a = get_all_kc()
    # a.get_all()
    # a = redis_conn.hget(1,1)
    # a = a.split('_')
    # p = {}
    # p['count'] = a[0]
    # p['price'] = a[1]
    # print(p)
    # a = redis_conn_slave.hgetall('sug_count')
    f = {'1':'1.0:./img/a.jpg','5':'1.0:./img/a.jpg'}
    t = [{'pid':k,'price':f[k].split(':')[0],'img':f[k].split(':')[1]} for k in f]
    print(t)
