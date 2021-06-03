#coding:utf-8
# 持仓模型

from . import db

class AccountOrder(db.Model):
    """ 账户模型 """
    __tablename__ = 'tb_account_order'
    account_id = db.Column(db.String(20), doc="用户ID", nullable=True)
    stock_name = db.Column(db.String(20), doc="股票名称", nullable=True)
    stock_code = db.Column(db.String(13), doc="代码",  primary_key=True)
    volume = db.Column(db.String(255), doc="持仓量", nullable=True)
    cost = db.Column(db.Float(5), doc="成本", nullable=True)
    
    def to_json(self):
        return {
            'account_id': self.account_id,
            'stock_name': self.stock_name,
            'stock_code': self.stock_code,
            'volume': self.volume,
            'cost': self.cost
        }