from io import BytesIO
import myproduct.venv.DAL as da
from myproduct.venv.Model.Redis_like import *
from flask import Blueprint, render_template, session, make_response, url_for
from myproduct.venv.Model.img import Captcha

index_ = Blueprint("index", __name__,url_prefix='/')  # 其中index是html蓝图中的名字
r_like = Rlike()


@index_.route('/')
def first():
    session.clear()
    return render_template('login.html')


@index_.route('/get_img')
def get_img():
    text, image = Captcha.gene_graph_captcha()
    print(text, image)
    out = BytesIO()
    image.save(out, 'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return resp


@index_.route('/index', methods=['GET'])
def index():
    # img = {'1':'a1.jpg', '2':'a2.jpg', '3':'a3.jpg', '4':'a4.jpg', '5':'a5.jpg'}
    img = {'1':'1.jpg', '2':'1.jpg', '3':'1.jpg', '4':'1.jpg', '5':'1.jpg'}
    if session['username']:
        return render_template('jiemian.html',url_username=session['username'],img=img,course=da.courseDAL.course_select_all())
    else:
        return render_template('login.html')


@index_.route('/discussion')
def discussion():
    sug = Suggestion()
    result = sug.get_all_suggestion()
    # print(result)
    like = r_like.if_like(result,session['username'])
    print(like)
    return render_template('pin_board.html',suggestion=result,like=like)


@index_.route('/like/<uid>')
def like(uid):
    r_like.like_user(uid,session['username'])
    print(r_like.get_count(uid))
    return str(r_like.get_count(uid))


@index_.route('/unlike/<uid>')
def unlike(uid):
    r_like.dis_like_user(uid,session['username'])
    return str(r_like.get_count(uid))


