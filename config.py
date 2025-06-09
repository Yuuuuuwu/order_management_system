import os

class BaseConfig:
    """共用設定"""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "replace-me")
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    # 可擴充更多共用設定

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