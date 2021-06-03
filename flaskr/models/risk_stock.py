#coding:utf-8
# 风险股票

from . import db

class RiskStock(db.Model):
    """ 风险股票模型 """
    __tablename__ = 'tb_risk_stock'
    stock_code = db.Column(db.String(8), primary_key=True, doc="股票ID")
    stock_name = db.Column(db.String(15), doc="股票名称", nullable=True)
    status = db.Column(db.String(255), nullable=True, doc="股票状态")
    status_desc = db.Column(db.String(255), nullable=True, doc="状态详情")
    create_time = db.Column(db.String(13), doc="添加时间", nullable=True, unique=True)
    
    def to_json(self):
        return {
            'stock_code': self.stock_code,
            'stock_name': self.stock_name,
            'status': self.status,
            'status_desc': self.status_desc,
            'create_time': self.create_time
        }
        
        
class RiskDegree(db.Model):
    """ 风险等级模型 """
    __tablename__ = 'tb_risk_degree'
    id = db.Column(db.String(255), primary_key=True, doc="ID")
    degree = db.Column(db.String(8), nullable=True, unique=True, doc="等级表述")
    
    def to_json(self):
        return {
            'id': self.id,
            'degree': self.degree
        }