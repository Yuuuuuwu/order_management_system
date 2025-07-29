# /home/jenny/0609/order_management_system/config.py
import os
from dotenv import load_dotenv

# 載入根目錄下的 .env 檔
load_dotenv(override=True, interpolate=True)

class BaseConfig:
    """共用設定"""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "replace-me")
    SECRET_KEY     = os.getenv("SECRET_KEY", "dev-secret-key")

    # 綠界支付參數
    ECPAY_MERCHANT_ID       = os.getenv("ECPAY_MERCHANT_ID")
    ECPAY_HASH_KEY          = os.getenv("ECPAY_HASH_KEY")
    ECPAY_HASH_IV           = os.getenv("ECPAY_HASH_IV")
    # Callback URL：綠界 server-to-server 通知
    ECPAY_NOTIFY_URL        = os.getenv("ECPAY_NOTIFY_URL")
    # Auto-Return 中繼 URL：綠界將 POST 自動導回到這裡
    ECPAY_ORDER_RETURN_URL  = os.getenv("ECPAY_ORDER_RETURN_URL")
    
    # 例外訊息往外傳遞，方便除錯  
    PROPAGATE_EXCEPTIONS = True  

    # 最後要把使用者 redirect 到前端的網址
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
    BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:5000")  

class DevelopmentConfig(BaseConfig):
    """開發環境設定"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://jenny:1234@db:3306/my_db"
    )

class TestingConfig(BaseConfig):
    """測試環境設定"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

class ProductionConfig(BaseConfig):
    """正式環境設定"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

class RenderConfig(BaseConfig):
    """Render 平台部署設定"""
    DEBUG = False
    
    # Render 提供的 PostgreSQL 資料庫 URL
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        # 修正 Render 的 PostgreSQL URL 格式（如果需要）
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        SQLALCHEMY_DATABASE_URI = database_url
    else:
        # 只有當環境為 render 時才需要 DATABASE_URL
        if os.getenv("FLASK_ENV") == "render":
            raise ValueError("DATABASE_URL environment variable is required for Render deployment")
        else:
            # 測試環境使用預設值
            SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    
    # Render 特殊設定
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_timeout': 20,
        'pool_size': 10,
        'max_overflow': 20,
    }
