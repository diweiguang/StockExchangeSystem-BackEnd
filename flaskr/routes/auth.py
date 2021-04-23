#coding:utf-8
# 认证路由

from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    return "login", 200

@auth_bp.route('/register', methods=['POST'])
def register():
    return "register", 200

@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    return "logout", 200