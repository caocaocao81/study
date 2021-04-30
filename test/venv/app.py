from dataclasses import dataclass
from flask import Flask
from flask import request,render_template,url_for,session,g,redirect

app = Flask(__name__, static_url_path="/")

app.config['SECRET_KEY'] = "dasdsafsddf"

@app.before_request
def before_request():
    g.user = None

@dataclass
class User:
    id: int
    name: str
    password: str


@app.route('/')
def first():
    return "hello"


@app.route('/login' , methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('email', None)
        password = request.form.get('password', None)
        print(username,password)
        if username == 'ctr@qq.com' and password == '123456':
            return render_template('profile.html')
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/profile')
def profile():
    if not g.user:
        return redirect(url_for('/login'))
    else:
        return render_template('profile.html')

# 该界面当做母版页
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/jiemian')
def jiemian():
    return render_template('jiemian.html')
app.run(host='127.0.0.1')