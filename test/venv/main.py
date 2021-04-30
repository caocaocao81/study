from flask import Flask, flash, get_flashed_messages
from flask import request,render_template,url_for,session,g,redirect
from flask_sqlalchemy import SQLAlchemy
import pymysql
import Redis


pymysql.install_as_MySQLdb()

app = Flask(__name__,static_url_path='/')

app.config['SECRET_KEY'] = "dasdsafsddf"  # 设置生成session ID
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/py_flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  # 实例化对象


@app.before_request
def before_user():
    # 过滤机制，如果没有登录或者页面不是登录页面则跳转到登录页面
    if request.path == '/login' or '/register':
        return None
    else:
        if 'username' in session:
            return None
        else:
            return render_template('login.html')


@app.route('/admin/<username>')
def change_information(username):
    uid = da.userDAL.user_select_uid_by_name(session['username'])
    print(uid)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 获得注册的相关信息
        username = request.form.get('name', None)
        password = request.form.get('pwd', None)
        password_check = request.form.get('pwd1', None)
        email = request.form.get('email', None)
        phone = request.form.get('phone', None)

        message = da.userDAL.user_insert(username, password,password_check, email, phone)  # 增加新用户
        # 弹框提示注册失败或者成功（弹框都未实现）
        flash(message)
        print(message)
        if message == "注册成功":
            session.clear()
            return render_template('register.html',message=message)
        else:
            return render_template('register.html',message=message)
    else:
        session.clear()
        return render_template('register.html')


@app.route('/register/success')
def node():
    return "注册成功"


@app.route('/login', methods=['GET','POST'])
def login():
    # img = {'1':'a1.jpg', '2':'a2.jpg', '3':'a3.jpg', '4':'a4.jpg', '5':'a5.jpg'}
    img = {'1': '1.jpg', '2': '1.jpg', '3': '1.jpg', '4': '1.jpg', '5': '1.jpg'}
    if request.method == 'POST':
        # 获得用户名和密码
        username = request.form.get('email', None)
        password = request.form.get('password', None)
        g.name = username
        print(username,password)
        session['username'] = username  # 获得用户名session
        # 设置十分钟的session存在时间
        message = da.userDAL.validate(username,password)
        flash(message)
        if da.userDAL.user_login(username,password):
            # return redirect(url_for('index',url_username=username))
            print(get_flashed_messages())
            return render_template('jiemian.html',url_username=g.name,img=img,course=da.courseDAL.course_select_all())
        else:
            print(message)
            return render_template('login.html',message=message)
    else:
        session.clear()  # 清空session
        return render_template('login.html')  # 返回登录界面


@app.errorhandler(404)
def not_found(error):  # 404
    return render_template('404.html'), 404


@app.errorhandler(500)
def error(error):
    return render_template('500.html'), 500


if __name__ == '__main__':
    import myproduct.venv.DAL as da
    from myproduct.venv.controller.index import *
    from myproduct.venv.controller.course import *
    from myproduct.venv.controller.mail import *
    app.register_blueprint(mail_)
    app.register_blueprint(index_)
    app.register_blueprint(cou)
    Redis.insert_mysql()

    app.run(host='127.0.0.1',debug=True)