#coding:utf-8
# 管理员模型
from . import db

class Manager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    phone = db.Column(db.String(13))
    password = db.Column(db.String(20))
    createTime = db.Column(db.DateTime())