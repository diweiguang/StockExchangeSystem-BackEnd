#coding:utf-8
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 初始化模型
def init_app(app):
    db.init_app(app)
    return db