#coding:utf-8
# 数据库方案（增删改查）
from . import db

def insert(data: object):
    """ 插入单个数据 """
    try:
        db.session.add(data)
        db.session.commit()
    except Exception as e:
        print(f'插入数据失败:{e}')
        
def insert_all(data: list):
    """ 插入批量数据 """
    try:
        db.session.add_all(data)
        db.session.commit()
    except Exception as e:
        print(f'插入批量数据失败:{e}')
        
def delete(data: object):
    """ 删除数据 """
    try:
        db.session.delete(data)
    except Exception as e:
        print(f'删除数据失败:{e}')