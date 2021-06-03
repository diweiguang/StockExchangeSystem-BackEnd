#coding:utf-8
# 账户模型

from . import db

class Account(db.Model):
    """ 账户模型 """
    __tablename__ = 'tb_account'
    id = db.Column(db.String(20), doc="ID", nullable=True)
    nickname = db.Column(db.String(20), doc="昵称", nullable=True)
    phone = db.Column(db.String(13), doc="手机号",  primary_key=True)
    password = db.Column(db.String(255), doc="密码", nullable=True)
    role = db.Column(db.String(5), doc="账户角色", nullable=True)
    create_time = db.Column(db.String(13), doc="注册时间", nullable=True)
    restAsset = db.Column(db.Float(), doc="剩余资产", nullable=True)
    profitAsset = db.Column(db.Float(), doc="盈亏资产", nullable=True)
    
    def to_json(self):
        return {
            'id': self.id,
            'nickname': self.nickname,
            'phone': self.phone,
            'password': self.password,
            'role': self.role,
            'create_time': self.create_time,
            'restAsset': self.restAsset,
            'profitAsset': self.profitAsset
        }