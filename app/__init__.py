# app/__init__.py
import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException
from config import Config
from marshmallow import ValidationError
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

# ------------ 全域 Swagger 設定 ------------
swagger_config = {
    "headers": [],
    "specs": [{
        "endpoint": "apispec",
        "route": "/apispec.json",
        "rule_filter": lambda rule: True,
        "model_filter": lambda tag: True
    }],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

template = {
    "swagger": "2.0",
    "info": {
        "title": "Order Management API",
        "version": "1.0",
        "description": "訂單管理系統 API"
    },
    "servers": [
        {"url": "http://localhost:5000", "description": "Development"}
    ],
    "components": {
        "schemas": {
            # 省略 schema 定義，請貼上你原本的 components.schemas
        },
        "securitySchemes": {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "輸入 'Bearer <ACCESS_TOKEN>'"
            }
        }
    },
    "security": [{"bearerAuth": []}]
}
# ------------------------------------------

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # 載入 Config
    env = os.getenv("FLASK_ENV", "development")
    cfg = {
        "development": DevelopmentConfig,
        "testing":    TestingConfig,
        "production": ProductionConfig
    }[env]
    app.config.from_object(cfg)

    # JWT 設定
    jwt = JWTManager(app)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            "code": 401,
            "message": "Token 已過期，請重新登入"
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(err_str):
        return jsonify({
            "code": 401,
            "message": "無效的 Token，請重新登入"
        }), 401

    @jwt.unauthorized_loader
    def missing_token_callback(err_str):
        return jsonify({
            "code": 401,
            "message": "缺少 Token，請先登入"
        }), 401

    # 初始化 ORM
    db.init_app(app)

    # 匯入所有 model（必須在 Migrate 之前導入，以便自動偵測）
    from app.models import User, Product, Order, OrderItem, Payment

    # 資料庫遷移
    Migrate(app, db)

    # Swagger
    from flasgger import Swagger
    Swagger(app)

    # 註冊各個 Blueprint
    from app.routes.main     import bp_main
    from app.routes.users    import bp_users
    from app.routes.orders   import bp_orders
    from app.routes.auth     import bp_auth
    from app.routes.products import bp_prod
    from app.routes.payments import bp_pay

    app.register_blueprint(bp_main)
    app.register_blueprint(bp_users)
    app.register_blueprint(bp_orders)
    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_prod)
    app.register_blueprint(bp_pay)

    # 全域錯誤處理
    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        return jsonify({
            "code": 400,
            "name": "Bad Request",
            "errors": e.messages
        }), 400

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        response = e.get_response()
        response.data = jsonify({
            "code": e.code,
            "name": e.name,
            "message": e.description
        }).data
        response.content_type = "application/json"
        return response

    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, HTTPException):
            return handle_http_exception(e)
        return jsonify({
            "code": 500,
            "name": "Internal Server Error",
            "message": str(e)
        }), 500

    return app
