#coding:utf-8
# 账户（自选股）模型

from . import db


class AccountStock(db.Model):
    """ 账户模型 """
    __tablename__ = 'tb_account_stock'
    # __table_args__ = {'extend_existing': True}
    id = db.Column(db.String(255), primary_key=True, doc="ID")
    account_id = db.Column(db.String(255), nullable=True, unique=True, doc="账户ID")
    stock_code = db.Column(db.String(8), nullable=True, unique=True, doc="股票ID")
    create_time = db.Column(db.String(13), doc="注册时间", nullable=True, unique=True)
    stock_name = db.Column(db.String(15), doc="股票名称", nullable=True)

    def to_json(self):
        return {
            'id': self.id,
            'account_id': self.account_id,
            'stock_code': self.stock_code,
            'create_time': self.create_time,
            'stock_name': self.stock_name
        }