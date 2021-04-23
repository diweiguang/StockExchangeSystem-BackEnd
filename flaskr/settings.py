#coding:utf-8
# 配置文件

class Config(object):
    """ 基础配置文件 """
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:hsy98106@127.0.0.1:3306/exchange_system'  # 数据库配置连接
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    
class DevelopmentConfig(Config):
    """ 开发环境 """
    ENV = 'development'    
    DEBUG = True
    
class ProductionConfig(Config):
    """ 生产环境 """
    ENV = 'production'   
    DEBUG = False 