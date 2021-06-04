#coding:utf-8
# 委托交易路由

from flask import Blueprint, request
from flaskr.models.account import Account
from flaskr.models.order import Order  # 订单模型
from flaskr.models.account_order import AccountOrder
from flaskr.models import db
from flaskr.utils import resp, pagination
import time

from flask import Blueprint

order_bp = Blueprint('order', __name__, url_prefix='/order')


@order_bp.route('/', methods=['GET'])
# @login_required
# 参数:account_id / status / pagelimit / pagenum
def order_list():
    """ 批量委托订单 """
    result = {'code': 200, 'msg': 'ok', 'data': {'order_list': [], 'sum': 0}}
    try:
        if request.args.get('account_id') is None or request.args.get(
                'status') is None or request.args.get(
                    'pagelimit') is None or request.args.get(
                        'pagenum') is None:
            raise Exception('参数错误！')
        limit, offset = pagination(int(request.args.get('pagelimit')),
                                   int(request.args.get('pagenum')))
        order_list = Order.query.filter(
            Order.account_id == request.args.get('account_id')).filter(
                Order.status == request.args.get('status')).order_by(
                    -Order.create_time).limit(limit).offset(offset).all()
        _sum = Order.query.filter(
            Order.account_id == request.args.get('account_id')
            and Order.status == request.args.get('status')).count()
        # 转化json格式
        if order_list is not None:
            for item in order_list:
                result['data']['order_list'].append(item.to_json())
            result['data']['sum'] = _sum
    except Exception as e:
        result['code'] = 500
        result['msg'] = f'批量委托订单错误:{e}'
    finally:
        return resp(result['code'], result['msg'], result['data'])


@order_bp.route('/', methods=['DELETE'])
# 参数：id
def delete_order():
    """ 删除委托订单 """
    result = {'code': 200, 'msg': 'ok', 'data': {}}
    try:
        if request.args.get('id') is None or request.args.get('account_id') is None:
            raise Exception('参数错误！')
        ass = Order.query.filter(Order.id == request.args.get('id')).first()
        
        account = db.session.query(Account).filter(
            Account.id == request.args.get('account_id')).first()
        # 计算资产
        fee = float(ass.volume * ass.price)
        fee = -1 * fee if request.args.get('direction') == 'buy' else fee
        account.restAsset = account.restAsset + fee
        ass.status = 3
        db.session.commit()
        if ass is None:
            raise Exception('未找到数据！')
        result['data'] = True
    except Exception as e:
        result['code'] = 500
        result['msg'] = f'删除委托订单:{e}'
    finally:
        return resp(result['code'], result['msg'], result['data'])


@order_bp.route('/', methods=['POST'])
# 参数：id
def add_order():
    """ 生成委托订单 """
    result = {'code': 200, 'msg': 'ok', 'data': {}}
    try:
        req = request.get_json()
        if req['account_id'] is None or req['stock_code'] is None or req[
                'stock_name'] is None or req['status'] is None or req[
                    'direction'] is None or req['volume'] is None or req[
                        'order_price'] is None or req['price'] is None:
            raise Exception('参数错误！')

        # 更新用户资产
        account = db.session.query(Account).filter(
            Account.id == req['account_id']).first()
        # 计算资产
        fee = float(req['volume']) * float(req['price'])
        fee = -1 * fee if req['direction'] == 'sell' else fee
        if account.restAsset < fee:
            raise Exception('资金余额不足！')
        account.restAsset = account.restAsset - fee

        now = round(time.time() * 1000)
        order = Order(id=f"{req['account_id']}{now}",
                      account_id=req['account_id'],
                      stock_code=req['stock_code'],
                      stock_name=req['stock_name'],
                      direction=req['direction'],
                      status=req['status'],
                      volume=req['volume'],
                      order_price=req['order_price'],
                      price=req['price'],
                      create_time=now)
        
        db.session.add(order)
        db.session.commit()
        result['data'] = order.to_json()
    except Exception as e:
        result['code'] = 500
        result['msg'] = f'生成委托订单:{e}'
    finally:
        return resp(result['code'], result['msg'], result['data'])


@order_bp.route('/account/orderlist', methods=['GET'])
# 参数: pagelimit / pagenum / account_id
def account_order():
    """ 持仓列表 """
    result = {'code': 200, 'msg': 'ok', 'data': {'order_list': [], 'sum': 0}}
    try:
        if request.args.get('pagelimit') is None or request.args.get(
                'pagenum') is None or request.args.get('account_id') is None:
            raise Exception('参数错误！')
        limit, offset = pagination(int(request.args.get('pagelimit')),
                                   int(request.args.get('pagenum')))
        order_list = db.session.query(AccountOrder).filter(
            AccountOrder.account_id == request.args.get(
                'account_id')).order_by(
                    AccountOrder.stock_code).limit(limit).offset(offset).all()
        _sum = db.session.query(AccountOrder).filter(
            AccountOrder.account_id == request.args.get('account_id')).count()
        # 转化json格式
        if order_list is not None:
            for item in order_list:
                result['data']['order_list'].append(item.to_json())
            result['data']['sum'] = _sum
    except Exception as e:
        result['code'] = 500
        result['msg'] = f'持仓列表错误:{e}'
    finally:
        return resp(result['code'], result['msg'], result['data'])


@order_bp.route('/account/detail', methods=['GET'])
# 参数: account_id / stock_code
def account_order_one():
    """ 持仓详情 """
    result = {'code': 200, 'msg': 'ok', 'data': {'order_list': [], 'sum': 0}}
    try:
        if request.args.get('stock_code') is None or request.args.get(
                'account_id') is None:
            raise Exception('参数错误！')
        order = db.session.query(AccountOrder).filter(
            AccountOrder.account_id == request.args.get('account_id')).filter(
                AccountOrder.stock_code == request.args.get(
                    'stock_code')).order_by(AccountOrder.stock_code).first()
        if order is not None:
            # 转化json格式
            result['data'] = order.to_json()
    except Exception as e:
        result['code'] = 500
        result['msg'] = f'持仓详情错误:{e}'
    finally:
        return resp(result['code'], result['msg'], result['data'])