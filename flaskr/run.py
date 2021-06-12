from flask import Flask, render_template
from flask_cors import CORS
# from flask_cache import Cache
import settings
import routes, models


def create_app():
    app = Flask(__name__,
                static_folder='../../client/dist/static',
                template_folder='../../client/dist')  # app核心对象

    # cache = Cache(config={'CACHE_TYPE': 'simple'})
    
    # 设置跨域请求
    CORS(app, supports_credentials=True)

    app.config.from_object(settings.DevelopmentConfig)  # 加载配置

    models.init_app(app)
    routes.init_app(app)
    # cache.init_app(app)

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


if __name__ == '__main__':
    app = create_app()
    app.run(host='localhost', port=5000)