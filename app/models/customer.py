from app import db  # 從 app 匯入 SQLAlchemy 實例，用來定義資料表
from sqlalchemy.orm import relationship  # 匯入 relationship，建立資料表關聯
from datetime import datetime, timezone  # 匯入 datetime，用來記錄時間欄位的預設值

# 定義 Customer 顧客資料表，繼承自 db.Model，讓 SQLAlchemy 知道這是資料表
class Customer(db.Model):
    __tablename__ = 'customers' # 指定資料表名稱為 customers
    id = db.Column(db.Integer, primary_key=True)    # 顧客唯一編號，整數型態，primary_key 表示主鍵、唯一、不可重複
    name = db.Column(db.String(64), nullable=False)  # 顧客姓名，字串最多 64 字元，nullable=False 表示必填
    phone = db.Column(db.String(32))
    address = db.Column(db.String(128))
    email = db.Column(db.String(64))
    tags = db.Column(db.String(128))  # 標籤，存成一整個字串，用逗號分隔，例如 "VIP,一級客戶"，方便快速分類 
    # 使用 Python 端管理時間，統一為 UTC 時區
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))  
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))  # 建立時間和更新時間，預設值為現在時間，onupdate 表示每次更新時自動更新為現在時間
    orders = relationship('Order', back_populates='customer')  # 關聯到 Order 訂單資料表，意思是「一個顧客可以有多筆訂單」
    # back_populates='customer' 表示 Order 資料表那邊也要設對應欄位叫 customer

    # 將資料轉成字典格式，方便前端或 API 回傳
    def to_dict(self):
        return {
            'id': self.id,  # 顧客編號
            'name': self.name,  # 姓名
            'phone': self.phone,  # 電話
            'address': self.address,  # 地址
            'email': self.email,  # 電子郵件
            'tags': self.tags.split(',') if self.tags else [],  
            # 標籤轉為陣列，如果有資料就用逗號切開，沒有資料回傳空陣列
            'created_at': self.created_at,  # 建立時間
            'updated_at': self.updated_at  # 更新時間
        }