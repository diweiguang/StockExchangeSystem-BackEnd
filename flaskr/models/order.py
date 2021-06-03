#coding:utf-8
# 委托列表

from . import db

class Order(db.Model):
    """ 风险股票模型 """
    __tablename__ = 'tb_order'
    id = db.Column(db.String(15), primary_key=True, doc="股票ID")
    account_id = db.Column(db.String(10), doc="账号ID")
    stock_code = db.Column(db.String(15), doc="股票编号", nullable=True)
    stock_name = db.Column(db.String(15), doc="股票名称", nullable=True)
    status = db.Column(db.String(255), nullable=True, doc="订单状态")
    direction = db.Column(db.String(5), nullable=True, doc="订单方向")
    volume = db.Column(db.Float(), nullable=True, doc="股票数量")
    price = db.Column(db.Float(), nullable=True, doc="股票价格")
    order_price = db.Column(db.Float(), nullable=True, doc="成交总价格")
    create_time = db.Column(db.String(13), doc="添加时间", nullable=True, unique=True)
    
    def to_json(self):
        return {
            'id': self.id,
            'account_id': self.account_id,
            'stock_code': self.stock_code,
            'stock_name': self.stock_name,
            'status': self.status,
            'direction': self.direction,
            'volume': self.volume,
            'price': self.price,
            'order_price': self.order_price,
            'create_time': self.create_time
        }
