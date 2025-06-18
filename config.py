import os

class BaseConfig:
    """共用設定"""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "replace-me")
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    # 可擴充更多共用設定

    # 綠界支付參數
    ECPAY_MERCHANT_ID = "3002607"
    ECPAY_HASH_KEY    = "pwFHCqoQZGmho4w6"
    ECPAY_HASH_IV     = "EkRm7iFT261dpevs"
    ECPAY_NOTIFY_URL = os.getenv("ECPAY_NOTIFY_URL", "https://8593-180-218-47-188.ngrok-free.app/payments/ecpay/callback")
    ECPAY_RETURN_URL = os.getenv("ECPAY_RETURN_URL", "http://localhost:5173/payments/payment_result")

class DevelopmentConfig(BaseConfig):
    """開發環境設定"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://jenny:1234@db:3306/my_db"  # Docker Compose 預設
    )

class TestingConfig(BaseConfig):
    """測試環境設定"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

class ProductionConfig(BaseConfig):
    """正式環境設定"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")