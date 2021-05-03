#coding:utf-8
# 功能函数
from flask import jsonify


def resp(code: int, msg: str, data):
    try:
        result = {
            'code': code,
            'msg': msg,
            'data': data
        }
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