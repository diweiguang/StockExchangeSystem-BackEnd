#coding:utf-8
# 股市(公司)路由

from flask import Blueprint, jsonify
from flaskr.services.stock_api import StockApi  # 开放接口
from flaskr.models.stocks import StockCompany  # 公司模型
from flaskr.models import db
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
    company = {}
    try:
        # 从数据库读取
        # company = StockApi.get_company(code)
        print(pagelimit)
    except Exception as e:
        print(f'get_stock_companies error: {e}')
    finally:
        return jsonify(company)


@stock_bp.route('/<string:code>', methods=['GET'])
def get_stock_company(code):
    """ 单一股票公司列表接口 """
    company = {}
    try:
        # 从数据库读取
        # company = StockApi.get_company(code)
        print(code)
    except Exception as e:
        print(f'get_stock_company error: {e}')
    finally:
        return jsonify(company)


@stock_bp.route('/real/<string:code>', methods=['GET'])
def get_stock_day(code):
    """ 股票实时数据接口 """
    stock = {}
    try:
        stock = StockApi.get_stock_real(code)
    except Exception as e:
        print(f'get_stock_day error: {e}')
    finally:
        return jsonify(stock)


@stock_bp.route('/trace/<string:code>', methods=['GET'])
def get_stock_trace(code):
    """ 买卖五档口数据接口 """
    trace5 = {}
    try:
        trace5 = StockApi.get_stock_trace5(code)
    except Exception as e:
        print(f'get_stock_trace error: {e}')
    finally:
        return jsonify(trace5)


@stock_bp.route('/timedeal/<string:code>', methods=['GET'])
def get_stock_daytimedeal(code):
    """ 当天分时数据数据接口 """
    timedeal = {}
    try:
        timedeal = StockApi.get_stock_daytimedeal(code)
    except Exception as e:
        print(f'get_stock_daytimedeal error: {e}')
    finally:
        return jsonify(timedeal)


@stock_bp.route('/timedeal/<string:code>/<string:level>', methods=['GET'])
def get_stock_realtimedeal(code, level):
    """ 当天分时数据数据接口 """
    timedeal = {}
    if level not in ['5', '15', '30', '60', 'Day', 'Week', 'Month', 'Year']:
        # 错误判断
        return jsonify({'error': 'level error'})
    try:
        timedeal = StockApi.get_stock_realtimedeal(code, level)
    except Exception as e:
        print(f'get_stock_realtimedeal error: {e}')
    finally:
        return jsonify(timedeal)


@stock_bp.route('/hist/timedeal/<string:code>/<string:level>', methods=['GET'])
def get_stock_hist_realtimedeal(code, level):
    """ 当天分时数据数据接口 """
    timedeal = {}
    if level not in ['5', '15', '30', '60', 'Day', 'Week', 'Month', 'Year']:
        # 错误判断
        return jsonify({'error': 'level error'})
    try:
        timedeal = StockApi.get_stock_hist_realtimedeal(code, level)
    except Exception as e:
        print(f'get_stock_hist_realtimedeal error: {e}')
    finally:
        return jsonify(timedeal)