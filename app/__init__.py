# app/__init__.py
# 匯入 Flask 相關套件
from flask import Flask, jsonify  # Flask 用來建立應用程式實例，jsonify 用來回傳 JSON 格式
from flask_sqlalchemy import SQLAlchemy  # SQLAlchemy 資料庫 ORM
from flask_migrate import Migrate  # 資料庫遷移工具
from flask_jwt_extended import JWTManager  # JWT 驗證管理
from flask_cors import CORS  # 處理跨域請求 (CORS)
from config import DevelopmentConfig, TestingConfig, ProductionConfig, RenderConfig  # 匯入自定義設定檔
import os  # 用來操作環境變數
from dotenv import load_dotenv  # 讀取 .env 檔案中的環境變數

load_dotenv()  # 載入 .env 檔案的環境變數

# 初始化 SQLAlchemy 實例
# 其他模組可以直接 from app import db，不會有循環 import 問題
db = SQLAlchemy()

# 自動匯入 models、schemas、services，確保 migrate 能正確找到所有資料表
import app.models.user, app.models.product, app.models.order, app.models.payment, app.models.customer, app.models.operation_log, app.models.notification# 匯入資料表模型
import app.schemas.user, app.schemas.product, app.schemas.order, app.schemas.payment, app.schemas.customer, app.schemas.notification  # 匯入 Marshmallow schema
import app.services.auth_service, app.services.user_service, app.services.product_service, app.services.order_service, app.services.payment_service, app.services.customer_service, app.services.report_service, app.services.notification_service  # 匯入服務層

# 工廠模式建立 app 實例
def create_app():
    app = Flask(__name__)  # 建立 Flask 應用程式實例

    env = os.getenv("FLASK_ENV", "development")  # 讀取環境變數 FLASK_ENV，預設為 development
    cfg_cls = {  # 根據環境選擇對應設定檔
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig,
        "render": RenderConfig
    }[env]
    app.config.from_object(cfg_cls)  # 載入對應設定檔

    db.init_app(app)  # 初始化 SQLAlchemy
    Migrate(app, db)  # 綁定資料庫遷移工具
    JWTManager(app)  # 啟用 JWT 管理

    # 設定 CORS，開發環境允許所有來源
    if env == "development":
        CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
    else:
        CORS(app, resources={r"/*": {"origins": app.config["FRONTEND_URL"]}}, supports_credentials=True)

    app.url_map.strict_slashes = False  # 關閉嚴格尾斜線檢查，避免 /api 和 /api/ 被視為不同路徑

    # 註冊 Blueprint 模組化路由
    from app.routes import auth, main, users, products, orders, payments, customers, dashboard, categories, reports, notifications  # 匯入各模組路由
    app.register_blueprint(auth.bp_auth)  # 註冊登入認證藍圖
    app.register_blueprint(main.bp_main)  # 註冊主頁相關藍圖
    app.register_blueprint(users.bp_users)  # 註冊使用者管理藍圖
    app.register_blueprint(products.bp_products)  # 註冊商品管理藍圖
    app.register_blueprint(orders.bp_orders)  # 註冊訂單管理藍圖
    app.register_blueprint(payments.bp_payments)  # 註冊付款管理藍圖
    app.register_blueprint(customers.bp_customers)  # 註冊顧客管理藍圖
    app.register_blueprint(dashboard.bp_dashboard)  # 匯入儀表板藍圖
    app.register_blueprint(categories.bp_categories)    # 匯入分類藍圖
    app.register_blueprint(reports.bp_reports)  # 匯入報表藍圖
    app.register_blueprint(notifications.bp_notifications)  # 匯入通知藍圖

    # 全域錯誤處理機制
    from marshmallow import ValidationError  # 匯入 schema 驗證錯誤
    from werkzeug.exceptions import HTTPException  # 匯入 HTTP 相關錯誤

    @app.errorhandler(ValidationError)  # 捕捉 schema 驗證錯誤
    def handle_validation_error(e):
        return jsonify({"code": 400, "name": "Bad Request", "errors": e.messages}), 400  # 回傳 400 錯誤和詳細資訊

    @app.errorhandler(HTTPException)  # 捕捉一般 HTTP 例外
    def handle_http_exception(e):
        response = e.get_response()  # 取得原始錯誤回應
        response.data = jsonify({
            "code": e.code,
            "name": e.name,
            "message": e.description
        }).data  # 修改回應為 JSON 格式
        response.content_type = "application/json"  # 設定回應類型
        return response  # 回傳處理後的錯誤回應

    @app.errorhandler(Exception)  # 捕捉所有未處理的例外
    def handle_exception(e):
        if isinstance(e, HTTPException):  # 如果是已知 HTTP 錯誤，使用上面的處理方式
            return handle_http_exception(e)
        return jsonify({
            "code": 500,
            "name": "Internal Server Error",
            "message": str(e)
        }), 500  # 其他未知錯誤回傳 500

    return app  # 回傳建立好的 app 實例
