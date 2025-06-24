# app/__init__.py
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import DevelopmentConfig, TestingConfig, ProductionConfig
import os
from dotenv import load_dotenv

load_dotenv()  # 載入 .env

# 初始化 SQLAlchemy
# 其他模組會從這裡 import db
# 這樣 models/* 可以直接 from app import db
# 不會有循環 import 問題

db = SQLAlchemy()

# 自動匯入 models/schemas/services，確保 migrate 能找到所有 model
import app.models.user, app.models.product, app.models.order, app.models.payment
import app.schemas.user, app.schemas.product, app.schemas.order, app.schemas.payment
import app.services.auth_service, app.services.user_service, app.services.product_service, app.services.order_service, app.services.payment_service
from app.routes.dashboard import bp_dashboard
from app.routes.categories import bp_categories
from .routes import reports_bp, notifications_bp

def create_app():
    app = Flask(__name__)
    env = os.getenv("FLASK_ENV", "development")
    cfg_cls = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
    }[env]
    app.config.from_object(cfg_cls)
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "replace-this-with-env")
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.debug = True

    db.init_app(app)
    Migrate(app, db)
    JWTManager(app)

    #CORS 改這裡，從 config 讀取 FRONTEND_URL
    CORS(app, resources={r"/*": {"origins": app.config["FRONTEND_URL"]}}, supports_credentials=True)
    # 關閉全域尾斜線嚴格檢查（就不會 302 redirect）
    app.url_map.strict_slashes = False

    # Blueprint 註冊
    from app.routes import auth, main, users, products, orders, payments, customers
    app.register_blueprint(auth.bp_auth)
    app.register_blueprint(main.bp_main)
    app.register_blueprint(users.bp_users)
    app.register_blueprint(products.bp_prod)
    app.register_blueprint(orders.bp_orders)
    app.register_blueprint(payments.bp_pay)
    app.register_blueprint(customers.bp_customers)
    app.register_blueprint(bp_dashboard)
    app.register_blueprint(bp_categories)
    app.register_blueprint(reports_bp)
    app.register_blueprint(notifications_bp)

    # 全域錯誤處理
    from marshmallow import ValidationError
    from werkzeug.exceptions import HTTPException
    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        return jsonify({"code": 400, "name": "Bad Request", "errors": e.messages}), 400
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        response = e.get_response()
        response.data = jsonify({"code": e.code, "name": e.name, "message": e.description}).data
        response.content_type = "application/json"
        return response
    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, HTTPException):
            return handle_http_exception(e)
        return jsonify({"code": 500, "name": "Internal Server Error", "message": str(e)}), 500

    return app
