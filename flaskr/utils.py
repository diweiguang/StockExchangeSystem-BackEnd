#coding:utf-8
# 功能函数

import functools
from flask import request, jsonify, current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from models.account import Account  # 账户模型
from models import db


def resp(code: int, msg: str, data):
    """ 返回函数 """
    try:
        result = {'code': code, 'msg': msg, 'data': data}
        return jsonify(result)
    except Exception as e:
        print(f'返回函数错误:{e}')


def pagination(pagelimit: int, pagenum: int) -> int:
    """ 分页 """
    try:
        offset = pagelimit * (pagenum - 1)
        return pagelimit, offset
    except Exception as e:
        print(f'分页函数错误: {e}')


#######################
# 用户身份验证
#######################


def valid_login(phone: str):
    """ 登陆验证 """
    result = True, ''
    try:
        if len(phone) != 11:
            raise Exception('手机格式错误')
    except Exception as e:
        result = False, e
    finally:
        return result


def valid_register(phone: str, password: str):
    """ 注册验证 """
    result = True, ''
    try:
        if len(phone) != 11:
            raise Exception('手机格式错误')
        if len(password) < 5:
            raise Exception('密码不能小于5位')
    except Exception as e:
        result = False, e
    finally:
        return result


def create_token(api_user):
    '''
    生成token
    :param api_user:用户id
    :return: token
    '''

    #第一个参数是内部的私钥，这里写在共用的配置信息里了，如果只是测试可以写死
    #第二个参数是有效期(秒)
    s = Serializer(current_app.config["SECRET_KEY"], expires_in=3600)
    #接收用户id转换与编码
    token = s.dumps({"id": api_user}).decode("ascii")
    return token


def verify_token(token):
    '''
    校验token
    :param token: 
    :return: 用户信息 or None
    '''

    #参数为私有秘钥，跟上面方法的秘钥保持一致
    s = Serializer(current_app.config["SECRET_KEY"])
    try:
        #转换为字典
        data = s.loads(token)
    except Exception:
        return None
    #拿到转换后的数据，根据模型类去数据库查询用户信息
    account = db.session.query(Account).filter(
        Account.phone == data['id']).one()
    return account.to_json()


#######################
# 装饰器
#######################


def login_required(func):
    @functools.wraps(func)
    def verify_token(*args, **kwargs):
        try:
            #在请求头上拿到token
            token = request.headers["token"]
        except Exception:
            #没接收的到token,给前端抛出错误
            #这里的code推荐写一个文件统一管理。这里为了看着直观就先写死了。
            return jsonify(code=4103, msg='缺少参数token')

        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            s.loads(token)
        except Exception:
            return jsonify(code=4101, msg="登录已过期")

        return func(*args, **kwargs)

    return verify_token
