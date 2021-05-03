from flask import Flask, render_template
from flask_cors import CORS
from . import settings
from . import routes, models


def create_app():
    app = Flask(__name__,
                static_folder='../../client/dist/static',
                template_folder='../../client/dist')  # app核心对象


    # 设置跨域请求
    CORS(app, supports_credentials=True)

    app.config.from_object(settings.DevelopmentConfig)  # 加载配置

    models.init_app(app)
    routes.init_app(app)

    # 配置首页路由
    @app.route('/', methods=['GET'])
    def index():
        return render_template('index.html')

    # 只能从前端跳转页面
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        return render_template("index.html")

    return app
