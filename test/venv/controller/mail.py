from flask import Blueprint, render_template, session, json, url_for
from myproduct.venv.Model.mail import *

mail_ = Blueprint('mail',__name__)  # 定义蓝图
mail = Mail()


@mail_.route('/mailbox',methods=['GET'])
def mailbox():  # 邮件箱
    result = mail.select_all_mail_by_user(session['username'])
    return render_template('mailbox.html',url_username=session['username'],result=result,mailcount=len(result))


@mail_.route('/mailbox/<mid>',methods=['GET'])
def mail_detail(mid):  # 邮件信息
    # 获得上一封下一封邮件以及邮件总数
    next,pre = mail.select_next_mail(session['username'],mid)
    result = mail.selecy_mail_by_user_mid(session['username'],mid)
    return render_template('mail_detail.html',result=result,next_mail=next,pre_mail=pre)


@mail_.route('/mail_del/<mid>')
def mail_del(mid):
    # 删除邮件
    del_inf = mail.del_mail_by_mid(mid,session['username'])
    print(mid,session['username'])
    print(del_inf)
    if del_inf == '删除成功':
        result = mail.select_all_mail_by_user(session['username'])
        return render_template('mailbox.html',result=result)
    else:
        return render_template('500.html'), 500
