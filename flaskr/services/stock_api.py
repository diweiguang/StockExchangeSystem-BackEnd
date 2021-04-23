import requests

class StockApi(object):
    license = '9F83CEA9-6399-A249-E1BC-94B317827892'
    
    @classmethod
    def get_stock_list(cls) -> list:
        """ 基础股票列表 """
        stock_list = []
        try:
            url = f'http://ig507.com/data/base/gplist?licence={cls.license}'
            resp = requests.get(url)
            if resp.status_code == 200:
                for item in resp.json():
                    stock_list.append({
                        'code': item['dm'],
                        'name': item['mc'],
                        'jys': item['jys']
                    })
        except Exception as e:
            print(f'股票基础列表错误:{e}')
        finally:
            return stock_list
        
    @classmethod
    def get_company(cls, stock: object) -> object:
        """ 公司简介 """
        company = {}
        code = stock['code']
        try:
            url = f'http://ig507.com/data/time/f10/info/{code}?licence={cls.license}'
            resp = requests.get(url)
            if resp.status_code == 200:
                data = resp.json()
                company = {
                    'code': code,
                    'stockname': stock['name'],
                    'jys': stock['jys'],
                    'name': data['name'],
                    'ename': data['ename'],
                    'market': None if data['market'] =='' else data['market'],
                    'idea': None if data['idea'] == '' else data['idea'],
                    'ldate': None if  data['ldate'] == '' else data['ldate'],
                    'sprice': None if  data['sprice'] == '' else data['sprice'],
                    'principal': None if  data['principal'] == '' else data['principal'],
                    'rdate': None if data['rdate'] == '' else data['rdate'],
                    'rprice': None if  data['rprice'] == '' else data['rprice'],
                    'instype': None if  data['instype'] == '' else data['instype'],
                    'organ': None if  data['organ'] == '' else data['organ'],
                    'phone': None if  data['phone'] == '' else data['phone'],
                    'site': None if  data['site'] == '' else data['site'],
                    'post': None if  data['post'] == '' else data['post'],
                    'addr': None if  data['addr'] == '' else data['addr'],
                    'oaddr': None if  data['oaddr'] == '' else data['oaddr'],
                    'desc': None if  data['desc'] == '' else data['desc']
                }
        except Exception as e:
            print(f'公司简介错误:{e}')
        finally:
            return company
            
    @classmethod
    def get_stock_real(cls, code: str) -> object:
        """ 股票实时数据 """
        stock = {}
        try:
            url = f'http://ig507.com/data/time/real/{code}?licence={cls.license}'
            resp = requests.get(url)
            if resp.status_code == 200:
                data = resp.json()
                print(data)
                stock = {
                    'fm': data['fm'],
                    'hs': data['hs'],
                    'lb': data['lb'],
                    'high': data['h'],
                    'low': data['l'],
                    'pc': data['pc'],
                    'sz': data['sz'],
                    'cje': data['cje'],
                    'ud': data['ud'],
                    'volume': data['v'],
                    't': data['t']
                }
        except Exception as e:
            print(f'股票实时数据错误:{e}')
        finally:
            return stock

    @classmethod
    def get_stock_trace5(cls, code: str) -> object:
        """ 买卖五档口数据 """
        trace5 = {}
        try:
            url = f'http://ig507.com/data/time/real/trace/level5/{code}?licence={cls.license}'
            resp = requests.get(url)
            if resp.status_code == 200:
                trace5 = resp.json()
        except Exception as e:
            print(f'买卖五档口数据错误:{e}')
        finally:
            return trace5
        
    @classmethod
    def get_stock_daytimedeal(cls, code: str) -> object:
        """ 当天分时成交数据 """
        deal = {}
        try:
            url = f'http://ig507.com/data/time/real/trace/timedeal/{code}?licence={cls.license}'
            resp = requests.get(url)
            if resp.status_code == 200:
                deal = resp.json()
        except Exception as e:
            print(f'当天分时成交数据错误:{e}')
        finally:
            return deal
        
    @classmethod
    def get_stock_realtimedeal(cls, code: str, level: str) -> object:
        """ 当天分时及级别成交数据 """
        deal = {}
        try:
            url = f'http://ig507.com/data/time/real/time/{code}/{level}?licence={cls.license}'
            resp = requests.get(url)
            if resp.status_code == 200:
                deal = resp.json()
        except Exception as e:
            print(f'当天分时及级别成交数据错误:{e}')
        finally:
            return deal
        
    @classmethod
    def get_stock_hist_realtimedeal(cls, code: str, level: str) -> object:
        """ 历史分时及级别成交数据 """
        deal = {}
        try:
            url = f'http://ig507.com/data/time/history/trade/{code}/{level}?licence={cls.license}'
            resp = requests.get(url)
            if resp.status_code == 200:
                deal = resp.json()
        except Exception as e:
            print(f'历史分时及级别成交数据错误:{e}')
        finally:
            return deal