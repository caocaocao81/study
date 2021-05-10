from flask import Blueprint, render_template, session, json, url_for, request,redirect
from myproduct.venv.Model.product import *
from myproduct.venv.Model.Redis_SecKill import *
from werkzeug.routing import BaseConverter

product_ = Blueprint('product',__name__)  # 定义蓝图
product = Product()


# class dictConverter(BaseConverter):
#     # {'Inventory': 100, 'pname': '一元课', 'img': './img/1.jpg',
#     #  'price': 1.0, 'pid': 1, 'description': '一元课程点击秒杀!!!'}
#     def to_python(self, value):
#         return value.split(',')
#     def to_url(self, values):
#         return ','.join(BaseConverter.to_url(self,value) for value in values)
@product_.route('/product')
def product_grid():
    result = product.select_all_product()
    print(result)
    return render_template('ecommerce_products_grid.html',result=result)


@product_.route('/product_detail/<pid>')
def product_detail(pid):
    name = 'product_'+str(pid)+'_kc'
    result = product.select_product_by_pid(pid)
    kc = redis_conn_slave.get(name)
    return render_template('ecommerce_product_detail.html',kc=kc,pid=pid,result=result)


@product_.route('/ccc/<pid>')
def ces(pid):
    # name = 'product_'+str(pid)+'_kc'
    kc = worker(pid,session['username'])
    return kc


@product_.route('/my_shopping_car')
def shopping_car(*args):
    # 展示用户购物车
    # 购物车数据放在redis中
    # 历史订单放在mysql中
    hash_name = session['username'] + '_products'
    user_product = redis_conn_slave.hgetall(hash_name)
    # 获得price和img
    # 分割数据 数据格式（price:img [1.0:./img/a.jpg]）
    total_price = 0
    user_product = [{'pid':k,'price': user_product[k].split(':')[0], 'img': user_product[k].split(':')[1]} for k in user_product]
    print(user_product)
    for i in user_product:
        total_price += float(i['price'])
    return render_template('ecommerce-cart.html',product=user_product,len=len(user_product),total_price=str(total_price))


@product_.route('/add_car/<pid>_<price>_<path:img>')
def add_car(pid,price,img):
    hash_name = session['username'] + '_products'
    # 判断是否添加过了
    # 添加过了就修改前端页面，让按钮不能添加,（修改数量）
    # 添加数量和价格(但是因为是课程所以不用考虑数量)
    price_img = str(price)+':'+str(img)
    if redis_conn.hsetnx(hash_name,pid,price_img):
        return "添加成功！"
    else:
        return "您已经添加过了！"


@product_.route('/remove/<pid>')
def remove(pid):
    hash_name = session['username'] + '_products'
    print('111')
    if redis_conn_slave.hexists(hash_name,pid):
        if redis_conn.hdel(hash_name,pid):
            print('删除成功')
            return '删除成功'
        else:
            print('删除失败')
            return '删除失败'
    else:
        print('购物车里面不存在')
        return '购物车里不存在该商品'


@product_.errorhandler(404)
def not_found(error):  # 404
    return render_template('404.html'), 404


@product_.errorhandler(500)
def error(error):
    return render_template('500.html'), 500