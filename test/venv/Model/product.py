from sqlalchemy import Table, MetaData, func
from myproduct.venv.main import db


class Product(db.Model):
    __table__ = Table('product', MetaData(bind=db.engine), autoload=True)

    def select_all_product(self):  # 获得所有商品
        result = db.session.query(Product).filter().all()
        db.session.close()
        result = self.change_data(result)
        return result

    def select_product_by_pid(self,pid):  # 通过pid获得商品
        result = db.session.query(Product).filter(Product.pid == pid).all()
        db.session.close()
        result = self.change_data(result)
        return result

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
#     product = Product()
#     result = product.select_product_by_pid(1)
#     print(result)