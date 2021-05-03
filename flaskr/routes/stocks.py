#coding:utf-8
# 股市行情(公司)路由

from operator import contains
from flask import Blueprint, jsonify
from flaskr.services.stock_api import StockApi  # 开放接口
from flaskr.models.stocks import StockCompany  # 公司模型
from flaskr.models import db
from flaskr.models.stocks import StockCompany
from flaskr.utils import resp, pagination
import time

stock_bp = Blueprint('stock', __name__, url_prefix='/stock')


@stock_bp.route('/update_stock', methods=['GET'])
def get_all_stocks():
    """ 
    手动获取市面最新数据。数据量较大
    股票（公司）列表接口 
    """
    stock_list = []
    stockcompany_list = []
    try:
        stock_list = StockApi.get_stock_list()
        for stock in stock_list:
            time.sleep(2)  # 限制请求频率
            stock_company = StockApi.get_company(stock)  # 获取公司详细信息
            sc = StockCompany(code=stock_company['code'],
                              stockname=stock_company['stockname'],
                              jys=stock_company['jys'],
                              name=stock_company['name'],
                              ename=stock_company['ename'],
                              market=stock_company['market'],
                              idea=stock_company['idea'],
                              ldate=stock_company['ldate'],
                              sprice=stock_company['sprice'],
                              principal=stock_company['principal'],
                              rdate=stock_company['rdate'],
                              rprice=stock_company['rprice'],
                              instype=stock_company['instype'],
                              organ=stock_company['organ'],
                              phone=stock_company['phone'],
                              site=stock_company['site'],
                              post=stock_company['post'],
                              addr=stock_company['addr'],
                              oaddr=stock_company['oaddr'],
                              desc=stock_company['desc'])
            db.session.add(sc)
            db.session.commit()
            print(sc.code)
        # 存储到数据库
    except Exception as e:
        print(f'get_all_stocks error: {e}')
    finally:
        return jsonify(stockcompany_list)


@stock_bp.route('/<int:pagelimit>/<int:pagenum>', methods=['GET'])
def get_stock_companies(pagelimit, pagenum):
    """ 批量股票公司列表接口 """
    result = {'code': 200, 'msg': 'ok', 'data': { 'companies': [], 'sum': 0}}
    try:
        # 分页
        limit, offset = pagination(pagelimit, pagenum)
        # 从数据库读取
        companies = StockCompany.query.order_by(
            StockCompany.code).limit(limit).offset(offset).all()
        _sum = StockCompany.query.count()
        # 转化json格式
        for item in companies:
            result['data']['companies'].append(item.to_json())
        result['data']['sum'] = _sum
    except Exception as e:
        result['code'] = 500
        result['msg'] = f'批量股票公司列表接口错误: {e}'
        print(result)
    finally:
        return resp(result['code'], result['msg'], result['data'])


@stock_bp.route('/<string:code>', methods=['GET'])
def get_stock_company(code):
    """ 单一股票公司列表接口 """
    result = {'code': 200, 'msg': 'ok', 'data': []}
    try:
        # 从数据库读取
        company = StockCompany.query.filter(StockCompany.code == code).first()
        if company is None:
            raise ValueError('公司信息不存在')
        result['data'] = company.to_json()
    except ValueError as e:
        result['code'] = 404
        result['msg'] = f'单一股票公司列表接口: {e}'
    except RuntimeError as e:
        result['code'] = 500
        result['msg'] = f'单一股票公司列表接口: {e}'
    finally:
        return resp(result['code'], result['msg'], result['data'])


@stock_bp.route('/real/<string:code>', methods=['GET'])
def get_stock_day(code):
    """ 股票实时数据接口 """
    result = {'code': 200, 'msg': 'ok', 'data': []}
    try:
        result['data'] = StockApi.get_stock_real(code)
    except Exception as e:
        result['code'] = 500
        result['msg'] = f'股票实时数据接口: {e}'
        print(result)
    finally:
        return resp(result['code'], result['msg'], result['data'])


@stock_bp.route('/trace/<string:code>', methods=['GET'])
def get_stock_trace(code):
    """ 买卖五档口数据接口 """
    result = {'code': 200, 'msg': 'ok', 'data': []}
    try:
        result['data'] = StockApi.get_stock_trace5(code)
    except Exception as e:
        result['code'] = 500
        result['msg'] = f'买卖五档口数据接口: {e}'
        print(result)
    finally:
        return resp(result['code'], result['msg'], result['data'])


@stock_bp.route('/timedeal/<string:code>', methods=['GET'])
def get_stock_daytimedeal(code):
    """ 当天分时数据接口 """
    result = {'code': 200, 'msg': 'ok', 'data': []}
    try:
        result['data'] = StockApi.get_stock_daytimedeal(code)
    except Exception as e:
        result['code'] = 500
        result['msg'] = f'当天分时数据接口: {e}'
        print(result)
    finally:
        return resp(result['code'], result['msg'], result['data'])


@stock_bp.route('/timedeal/<string:code>/<string:level>', methods=['GET'])
def get_stock_realtimedeal(code, level):
    """ 当天分时实时数据接口 """
    result = {'code': 200, 'msg': 'ok', 'data': []}
    if level not in ['5', '15', '30', '60', 'Day', 'Week', 'Month', 'Year']:
        raise Exception('level 错误')  # 错误判断
    try:
        result['data'] = StockApi.get_stock_realtimedeal(code, level)
    except Exception as e:
        result['code'] = 500
        result['msg'] = f'当天分时实时数据接口: {e}'
        print(result)
    finally:
        return resp(result['code'], result['msg'], result['data'])


@stock_bp.route('/hist/timedeal/<string:code>/<string:level>', methods=['GET'])
def get_stock_hist_realtimedeal(code, level):
    """ 历史分时数据接口 """
    result = {'code': 200, 'msg': 'ok', 'data': []}
    if level not in ['5', '15', '30', '60', 'Day', 'Week', 'Month', 'Year']:
        raise Exception('level 错误')  # 错误判断
    try:
        result['data'] = StockApi.get_stock_hist_realtimedeal(code, level)
    except Exception as e:
        result['code'] = 500
        result['msg'] = f'历史分时数据接口: {e}'
        print(result)
    finally:
        return resp(result['code'], result['msg'], result['data'])
    
@stock_bp.route('/week/updown', methods=['GET'])
def get_stock_week_updown():
    """ 周涨跌数据接口 """
    result = {'code': 200, 'msg': 'ok', 'data': []}
    try:
        result['data'] = StockApi.get_updown_week()
    except Exception as e:
        result['code'] = 500
        result['msg'] = f'周涨跌数据接口: {e}'
        print(result)
    finally:
        return resp(result['code'], result['msg'], result['data'])
    
@stock_bp.route('/month/updown', methods=['GET'])
def get_stock_month_updown():
    """ 月涨跌数据接口 """
    result = {'code': 200, 'msg': 'ok', 'data': []}
    try:
        result['data'] = StockApi.get_updown_month()
    except Exception as e:
        result['code'] = 500
        result['msg'] = f'月涨跌数据接口: {e}'
        print(result)
    finally:
        return resp(result['code'], result['msg'], result['data'])