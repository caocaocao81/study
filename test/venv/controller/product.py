from flask import Blueprint, render_template, session, json, url_for, request,redirect
from myproduct.venv.Model.product import *
from myproduct.venv.Model.Redis_SecKill import *

product_ = Blueprint('product',__name__)  # 定义蓝图
product = Product()


@product_.route('/product')
def product_grid():
    result = product.select_all_product()
    print(result)
    return render_template('ecommerce_products_grid.html',result=result)


@product_.route('/product_detail/<pid>')
def product_detail(pid):
    name = 'product_'+str(pid)+'_kc'
    kc = redis_conn.get(name)
    return render_template('ecommerce_product_detail.html',kc=kc,pid=pid)


@product_.route('/ccc/<pid>')
def ces(pid):
    # name = 'product_'+str(pid)+'_kc'
    kc = worker(pid,session['username'])
    return kc