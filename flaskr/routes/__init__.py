from .auth.auth import auth_bp
from .auth.quote import quote_bp
from .auth.risk import risk_bp
from .auth.order import order_bp
from .pub.stocks import stock_bp

def init_app(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(stock_bp)
    app.register_blueprint(quote_bp)
    app.register_blueprint(risk_bp)
    app.register_blueprint(order_bp)
