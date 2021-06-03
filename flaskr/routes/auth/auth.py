#coding:utf-8
# 认证（登录/注册）路由

from flask import Blueprint, request, session
from flaskr.models.account import Account  # 账户模型
from flaskr.models import db
from flaskr.utils import create_token, login_required, resp, valid_login, valid_register, verify_token, pagination
import time

from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['POST'])
def login():
    """ 登录 """
    result = {'code': 200, 'msg': 'ok', 'data': {}}
    try:
        req = request.get_json()  # 接收前端数据Json格式
        account = valid_login(req['phone'])
        if account[0]:  # 电话格式合法
            account = db.session.query(Account).filter(
                Account.phone == req['phone'],
                Account.password == req['password']).first()
            if account is None:
                raise Exception('账户或密码错误！')
            # 用户存在，创建token
            token = create_token(account.phone)
            session['token'] = token
            result['data'] = {'token': token}
            print(session)
        else:
            raise Exception(account[1])
    except Exception as e:
        result['code'] = 500
        result['msg'] = f'登录错误:{e}'
    finally:
        return resp(result['code'], result['msg'], result['data'])


@auth_bp.route('/register', methods=['POST'])
def register():
    """ 注册 """
    result = {'code': 200, 'msg': 'ok', 'data': {}}
    try:
        req = request.get_json()
        register = valid_register(req['phone'], req['password'])
        if register[0]:  # 数据是否合法
            account = repeat_register(req['phone'])
            if account[0]:  # 账户不存在
                account = Account(nickname=req['nickname'],
                                  phone=req['phone'],
                                  password=req['password'],
                                  role='user',
                                  createTime=round(time.time() * 1000))
                db.session.add(account)
                db.session.commit()
                result['data'] = account.to_json()
            else:
                raise Exception(account[1])
        else:
            raise Exception(register[1])
    except Exception as e:
        result['code'] = 500
        result['msg'] = f'注册错误:{e}'
    finally:
        return resp(result['code'], result['msg'], result['data'])


@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    """ 登出 """
    result = {'code': 200, 'msg': 'ok', 'data': {}}
    try:
        session.pop('token', None)
    except Exception as e:
        result['code'] = 500
        result['msg'] = f'登出错误:{e}'
    finally:
        return resp(result['code'], result['msg'], result['data'])


@auth_bp.route('/userInfo', methods=['GET'])
@login_required
def userInfo():
    """ 用户信息 """
    token = request.headers["token"]
    #拿到token，去换取用户信息
    return resp(200, 'ok', verify_token(token))

@auth_bp.route('/userlist', methods=['GET'])
# 参数:pagelimit / pagenum
def userList():
    """ 用户列表 """
    result = {'code': 200, 'msg': 'ok', 'data': {'account_list': [], 'sum': 0}}
    try:
        if request.args.get('pagelimit') is None or request.args.get('pagenum') is None:
            raise Exception('参数错误！')
        limit, offset = pagination(int(request.args.get('pagelimit')),
                                   int(request.args.get('pagenum')))
        account_list = Account.query.filter(Account.role == 'user').order_by(Account.create_time).limit(limit).offset(offset).all()
        _sum = Account.query.filter(Account.role == 'user').count()
        # 转化json格式
        if account_list is not None:
            for item in account_list:
                result['data']['account_list'].append(item.to_json())
            result['data']['sum'] = _sum
    except Exception as e:
        result['code'] = 500
        result['msg'] = f'登出错误:{e}'
    finally:
        return resp(result['code'], result['msg'], result['data'])


@auth_bp.route('/user', methods=['DELETE'])
# @login_required
# 参数：id
def delete_user():
    """ 删除自选股 """
    result = {'code': 200, 'msg': 'ok', 'data': {}}
    try:
        if request.args.get('id') is None:
            raise Exception('参数错误！')
        ass = Account.query.filter(
            Account.id == request.args.get('id')).first()
        # db.session.delete(ass)
        # db.session.commit()
        if ass is None:
            raise Exception('未找到数据！')
        result['data'] = True
    except Exception as e:
        result['code'] = 500
        result['msg'] = f'删除用户错误:{e}'
    finally:
        return resp(result['code'], result['msg'], result['data'])

############################################
# 辅助函数
############################################


def repeat_register(phone: str):
    """ 判断用户是否已经存在，存在False，不存在True """
    try:
        account = db.session.query(Account).filter(
            Account.phone == phone).first()
        if account is None:
            return True, ''
        raise Exception('手机号已注册！')
    except Exception as e:
        return False, e