#coding:utf-8
# 风险管理

from re import S
from flask import Blueprint, request
from models.risk_stock import RiskStock, RiskDegree
from models.stocks import StockCompany
from models import db
from utils import resp, pagination
import time

from flask import Blueprint

risk_bp = Blueprint('risk', __name__, url_prefix='/risk')


@risk_bp.route('/stocklist', methods=['GET'])
# 参数:pagelimit / pagenum
def risk_stock():
    """ 风险列表 """
    result = {'code': 200, 'msg': 'ok', 'data': {'stock_list': [], 'sum': 0}}
    try:
        if request.args.get('pagelimit') is None or request.args.get(
                'pagenum') is None:
            raise Exception('参数错误！')
        limit, offset = pagination(int(request.args.get('pagelimit')),
                                   int(request.args.get('pagenum')))
        stock_list = db.session.query(RiskStock).join(
            RiskDegree, RiskDegree.id == RiskStock.status).order_by(-
                RiskStock.create_time).limit(limit).offset(offset).all()
        _sum = db.session.query(RiskStock).count()
        # 转化json格式
        if stock_list is not None:
            for item in stock_list:
                result['data']['stock_list'].append(item.to_json())
            result['data']['sum'] = _sum
    except Exception as e:
        result['code'] = 500
        result['msg'] = f'风险股票错误:{e}'
    finally:
        return resp(result['code'], result['msg'], result['data'])
    
@risk_bp.route('/stock', methods=['GET'])
# 参数: stock_code
def risk_stock_one():
    """ 风险股票 """
    result = {'code': 200, 'msg': 'ok', 'data': {}}
    try:
        if request.args.get('stock_code') is None:
            raise Exception('参数错误！')
        stock = db.session.query(RiskStock).filter(RiskStock.stock_code == request.args.get('stock_code')).first()
        if stock is not None:
            result['data'] = stock.to_json()
    except Exception as e:
        result['code'] = 500
        result['msg'] = f'风险股票错误:{e}'
    finally:
        return resp(result['code'], result['msg'], result['data'])

@risk_bp.route('/stocklist', methods=['POST'])
# 参数: stock_code / stock_name / status / status_desc
def add_risk_stock():
    """ 添加风险股票 """
    result = {'code': 200, 'msg': 'ok', 'data': {}}
    try:
        req = request.get_json()
        if req.get('stock_code') is None or req.get(
                'stock_name') is None or req.get('status') is None or req.get(
                    'status_desc') is None:
            raise Exception('参数错误！')
        stock = repeat_stock(req.get('stock_code'))
        if stock[0]:  # 股票未重复
            riskStock = RiskStock(stock_code=req.get('stock_code'),
                                  stock_name=req.get('stock_name'),
                                  status=req.get('status'),
                                  status_desc=req.get('status_desc'),
                                  create_time=round(time.time() * 1000))
            db.session.add(riskStock)
            db.session.commit()
            result['data'] = riskStock.to_json()
        else:
            raise Exception(stock[1])
    except Exception as e:
        result['code'] = 500
        result['msg'] = f'添加风险股票错误:{e}'
    finally:
        return resp(result['code'], result['msg'], result['data'])


@risk_bp.route('/stocklist', methods=['DELETE'])
# 参数: stock_code
def delete_risk_stock():
    """ 风险股票删除 """
    result = {'code': 200, 'msg': 'ok', 'data': {}}
    try:
        print(request.args)
        print(request.get_data())
        if request.args.get('stock_code') is None:
            raise Exception('参数错误！')
        ass = RiskStock.query.filter(
            RiskStock.stock_code == request.args.get('stock_code')).first()
        db.session.delete(ass)
        db.session.commit()
        if ass is None:
            raise Exception('未找到数据！')
        result['data'] = True
    except Exception as e:
        result['code'] = 500
        result['msg'] = f'删除风险股票错误:{e}'
    finally:
        return resp(result['code'], result['msg'], result['data'])


############################################
# 辅助函数
############################################


def repeat_stock(stock_code: str):
    """ 判断股票是否已经存在，存在False，不存在True """
    try:
        # 查询股票是否已经添加
        riskStock = db.session.query(RiskStock).filter(
            RiskStock.stock_code == stock_code).first()
        if riskStock is None:
            return True, ''
        raise Exception('风险股票已添加！')
    except Exception as e:
        return False, e