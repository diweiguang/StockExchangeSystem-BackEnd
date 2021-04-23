from flask import Flask, render_template
from . import settings
from . import routes, models


def create_app():
    app = Flask(__name__,
                # instance_relative_config=True
                # static_folder='../../client/dist/static',
                # template_folder='../../client/dist'
                )  # app核心对象
    
    app.config.from_object(settings.DevelopmentConfig)  # 加载配置

    models.init_app(app)
    routes.init_app(app)

    # # 配置首页路由
    # @app.route('/', methods=['GET'])
    # def index():
    #     return render_template('index.html')

    # # 只能从前端跳转页面
    # @app.route('/', defaults={'path': ''})
    # @app.route('/<path:path>')
    # def catch_all(path):
    #     return render_template("index.html")

    return app
