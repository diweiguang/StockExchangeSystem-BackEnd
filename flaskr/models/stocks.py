#coding:utf-8
# 股票（公司）模型
from . import db
    
    
class StockCompany(db.Model):
    """ 公司模型 """
    __tablename__ = 'stock_company'
    code = db.Column(db.String(8), primary_key=True)
    stockname = db.Column(db.String(15), doc="股票名称", unique=True, nullable=True)
    jys = db.Column(db.String(3), doc="交易所", nullable=True)
    name = db.Column(db.String(255), doc="公司名称", unique=True, nullable=True)
    ename = db.Column(db.String(255), doc="公司英文名称", unique=True, nullable=True)
    market = db.Column(db.String(255), doc="上市市场")
    idea = db.Column(db.String(255), doc="概念及板块")
    ldate = db.Column(db.String(255), doc="上市日期")
    sprice = db.Column(db.String(255), doc="发行价格")
    principal = db.Column(db.String(255), doc="主承商")
    rdate = db.Column(db.String(255), doc="成立日期")
    rprice = db.Column(db.String(255), doc="注册资本")
    instype = db.Column(db.String(255), doc="机构类型")
    organ = db.Column(db.String(255), doc="组织形式")
    phone = db.Column(db.String(255), doc="公司电话")
    site = db.Column(db.String(255), doc="公司网站")
    post = db.Column(db.String(255), doc="邮政编码")
    addr = db.Column(db.String(255), doc="注册地址")
    oaddr = db.Column(db.String(255), doc="办公地址")
    desc = db.Column(db.Text(), doc="公司简介")