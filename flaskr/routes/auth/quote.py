#coding:utf-8
# 自选股路由

from flask import Blueprint, request
from flaskr.models.account_stock import AccountStock  # 账户(自选股)模型
from flaskr.models import db
from flaskr.utils import resp, pagination
import time

from flask import Blueprint

quote_bp = Blueprint('quote', __name__, url_prefix='/quote')


# /<string:account_id>/<int:pagelimit>/<int:pagenum>
@quote_bp.route('/', methods=['GET'])
# @login_required
# 参数:account_id / pagelimit / pagenum
def stock_list():
    """ 批量自选股 """
    result = {'code': 200, 'msg': 'ok', 'data': {'stock_list': [], 'sum': 0}}
    try:
        if request.args.get('account_id') is None or request.args.get(
                'pagelimit') is None or request.args.get('pagenum') is None:
            raise Exception('参数错误！')
        limit, offset = pagination(int(request.args.get('pagelimit')),
                                   int(request.args.get('pagenum')))
        stock_list = AccountStock.query.filter(
            AccountStock.account_id == request.args.get(
                'account_id')).order_by(
                    AccountStock.stock_code).limit(limit).offset(offset).all()
        _sum = AccountStock.query.filter(
            AccountStock.account_id == request.args.get('account_id')).count()
        # 转化json格式
        if stock_list is not None:
            for item in stock_list:
                result['data']['stock_list'].append(item.to_json())
            result['data']['sum'] = _sum
    except Exception as e:
        result['code'] = 500
        result['msg'] = f'批量自选股错误:{e}'
    finally:
        return resp(result['code'], result['msg'], result['data'])


@quote_bp.route('/', methods=['POST'])
# @login_required
# 参数：account_id / stock_code / stock_name
def add_stock():
    """ 添加自选股 """
    result = {'code': 200, 'msg': 'ok', 'data': {}}
    try:
        req = request.get_json()
        if req['account_id'] is None or req['stock_code'] is None or req[
                'stock_name'] is None:
            raise Exception('参数错误！')
        account_stock = find_account_stock(req['account_id'],
                                           req['stock_code'])
        if account_stock[0]:
            # req = request.get_json()
            now = round(time.time() * 1000)
            ass = AccountStock(id=f"{req['account_id']}{now}",
                               account_id=req['account_id'],
                               stock_code=req['stock_code'],
                               create_time=now,
                               stock_name=req['stock_name'])
            db.session.add(ass)
            db.session.commit()
            result['data'] = ass.to_json()
        else:
            raise Exception(account_stock[1])
    except Exception as e:
        result['code'] = 500
        result['msg'] = f'添加自选股错误:{e}'
    finally:
        return resp(result['code'], result['msg'], result['data'])


@quote_bp.route('/', methods=['DELETE'])
# @login_required
# 参数：id
def delete_stock():
    """ 删除自选股 """
    result = {'code': 200, 'msg': 'ok', 'data': {}}
    try:
        if request.args.get('id') is None:
            raise Exception('参数错误！')
        ass = AccountStock.query.filter(
            AccountStock.id == request.args.get('id')).first()
        db.session.delete(ass)
        db.session.commit()
        if ass is None:
            raise Exception('未找到数据！')
        result['data'] = True
    except Exception as e:
        result['code'] = 500
        result['msg'] = f'删除自选股错误:{e}'
    finally:
        return resp(result['code'], result['msg'], result['data'])


############################################
# 辅助函数
############################################


def find_account_stock(account_id, stock_code):
    try:
        ass = AccountStock.query.filter(
            AccountStock.account_id == account_id,
            AccountStock.stock_code == stock_code).first()
        if ass is None:
            return True, ''
        raise Exception('该账户已选过该股票！')
    except Exception as e:
        return False, e