from .auth import auth_bp
from .stocks import stock_bp

def init_app(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(stock_bp)
