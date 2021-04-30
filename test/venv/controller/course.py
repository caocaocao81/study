from flask import Blueprint, render_template, session, json
import myproduct.venv.DAL as da
from myproduct.venv.Model.user import *
cou = Blueprint("course",__name__)


@cou.route('/course/information',methods=['GET'])
def course_ajax():
    result = da.courseDAL.course_select_all()
    result_json = json.dumps(result,ensure_ascii=False)
    # print(result_json)
    return result_json


@cou.route('/note',methods=['POST'])
def getnode():
    return 'aaa'


@cou.route('/course/<cname>', methods=['GET'])
def course(cname):
    if session['username']:
        print(cname)
        # 以按钮为控制，控制每一节课的视频和介绍不同
        user_node = da.courseDAL.course_select_by_name_like(cname)
        print(user_node)
        # 写一个选择查出用户个人笔记 session
        user = User()
        result = user.select_user_note(session['username'])
        print(type(user_node[0]['movie']))
        return render_template('course.html', user_node=user_node[0]['introduce'],
                               url_username=session['username'], result=result,movie=user_node)
    else:
        return render_template('login.html')

# @cou.route('/course', methods=['GET'])
# def course():
#     if session['username']:
#         # 以按钮为控制，控制每一节课的视频和介绍不同
#         user_node = da.courseDAL.course_select_by_name_like('第一讲')
#         # 写一个选择查出用户个人笔记 session
#         user = User()
#         result = user.select_user_note(session['username'])
#         print(result)
#         return render_template('course.html', user_node=user_node[0]['introduce'],
#                                url_username=session['username'], result=result)
#     else:
#         return render_template('login.html')