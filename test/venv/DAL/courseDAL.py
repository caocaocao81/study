from myproduct.venv.Model.course import Course


# 获取课程所有数据
def course_select_by_name(name):
    course = Course()
    row = course.select_course_by_name(name)
    list = course.change_data(row)
    return list


def course_select_by_name_like(name):  # 根据课程名模糊查找
    course = Course()
    row = course.select_course_by_name_like(name)
    list = course.change_data(row)
    return list


def course_select_all():  # 获得所有课程（用于获得课程字典）
    course = Course()
    result = course.select_course_all()
    result_change = course.change_data(result)
    return result_change


