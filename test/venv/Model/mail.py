from sqlalchemy import Table, MetaData, func
from myproduct.venv.main import db


class Mail(db.Model):  # 邮箱类
    __table__ = Table('mail',MetaData(bind=db.engine),autoload=True)

    def select_all_mail_by_user(self,username):  # 获得所有邮件
        result = db.session.query(Mail).filter(Mail.uname == username).all()
        db.session.close()
        result = self.change_data(result)
        return result

    def selecy_mail_by_user_mid(self,username,mid):  # 获得某封邮件信息
        result = db.session.query(Mail).filter(Mail.uname ==username,Mail.id ==mid).all()
        db.session.close()
        result = self.change_data(result)
        return result

    def select_next_mail(self,username,mid):  # 下一封邮件
        result = self.select_all_mail_by_user(username)
        l = len(result)
        print(l)
        for i in range(l):
            if result[i]['id'] == int(mid):  # 导入的mid为str类型
                if i == 0 and i+1 == l:
                    return '已经没有邮件了哦！','前面已经没有邮件哦！'
                if i == 0:
                    return result[i+1],'前面已经没有邮件哦！'
                if i+1 == l:
                    return '已经没有邮件了哦！',result[i-1]
                return result[i+1],result[i-1]

    def del_mail_by_mid(self,mid,username):
        try:
            db.session.delete(db.session.query(Mail).
                              filter(Mail.uname == username,
                                     Mail.id == mid).first())
            db.session.commit()
        except:
            db.session.rollback()
            return '出错了!'
        db.session.close()
        return '删除成功'

    def change_data(self,row):
        list = []
        for r in row:
            dict = {}
            for k, v in r.__dict__.items():
                if not k.startswith('_sa_instance_state'):
                    dict[k] = v
            list.append(dict)
        return list


# if __name__ == '__main__':
#     mail = Mail()
#     # a = mail.selecy_mail_by_user_mid('452','1')
#     # print(mail.del_mail_by_mid(['2'],'450'))
#     a,b= mail.select_next_mail('452','1')
#     print(a)
#     print(b)