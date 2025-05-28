import os
from datetime import timedelta

class Config:
    # MySQL 資料庫連線字串：
    # 格式：mysql+pymysql://<使用者名稱>:<密碼>@<主機>/<資料庫名稱>
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://jenny:1234@localhost/order_management'
    # 關閉 SQLAlchemy 的修改追蹤功能，可減少不必要的記憶體與效能負擔
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "replace-me")  # 一定要有

    # 預設 token 失效時間（小時）
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES_HOURS", "1")))

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    # 開發時延長到 7 天
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES_DAYS", "7")))

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://jenny:1234@db:3306/my_db"
    )

class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

class ProductionConfig(BaseConfig):
    DEBUG = False
    # 由環境變數 DATABASE_URL 提供，若沒有就報錯
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
