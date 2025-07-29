from app import db  # 匯入 SQLAlchemy 的資料庫實例（db = SQLAlchemy(app)）
from datetime import datetime, timezone  # 用來建立時間欄位（含時區）
from app.models.user import User  # 匯入 User 模型，用來建立關聯

class Order(db.Model):  # 訂單主表
    """訂單資料表"""
    __tablename__ = 'orders'  # 指定在資料庫中對應的表格名稱為 'orders'

    id = db.Column(db.Integer, primary_key=True)  # 主鍵，自動遞增
    order_sn = db.Column(db.String(64), unique=True, nullable=False)  # 訂單編號，必填且不可重複
    trade_no = db.Column(db.String(20), unique=True, nullable=True)  # 交易編號
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='RESTRICT'), nullable=False)  # 對應 user 表的 id（外鍵），不可為空
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id', ondelete='SET NULL'), nullable=True)  # 對應 customer 表的 id（可空）
    total_amount = db.Column(db.Float, nullable=False)  # 總金額，必填
    status = db.Column(db.String(20), default='pending', nullable=False)  # 訂單狀態，預設為 pending
    shipping_fee = db.Column(db.Float, default=0, nullable=False)  # 運費，預設為 0
    payment_status = db.Column(db.String(20), default='unpaid', nullable=False)  # 付款狀態，預設為未付款
    remark = db.Column(db.Text)  # 備註（可空）
    receiver_name = db.Column(db.String(120), nullable=False)  # 收件人姓名
    receiver_phone = db.Column(db.String(40), nullable=False)  # 收件人電話
    shipping_address = db.Column(db.String(255), nullable=False)  # 收件地址
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc), nullable=True)  # 更新可以允許空

    # 資料表關聯設定
    items = db.relationship('OrderItem', backref='order', lazy='selectin', cascade="all, delete-orphan")  # 一對多：訂單 ➜ 多筆商品明細
    histories = db.relationship('OrderHistory', backref='order', lazy='selectin', cascade="all, delete-orphan")  # 一對多：訂單 ➜ 多筆歷史紀錄
    customer = db.relationship('Customer', back_populates='orders')  # 多對一：訂單 ➜ 客戶，需配對 Customer.orders
    user = db.relationship('User', back_populates='orders', lazy='selectin')  # 多對一：訂單 ➜ 使用者，需配對 User.orders

    def to_dict(self, include_items=False, include_history=False, include_user=False):  # 將 Order 物件轉為字典格式，方便前端使用
        """轉換為 dict，可選擇是否包含明細、歷史、使用者資料"""
        
        data = {
            "id": self.id,  # 訂單的唯一編號（主鍵）
            "order_sn": self.order_sn,  # 訂單編號（像是 20240708001）
            "user_id": self.user_id,  # 該訂單的下單者 ID（來自 users 表）
            "customer_id": self.customer_id,  # 該訂單的收件人（可選填，例如實際收件人可能非會員）
            "total_amount": self.total_amount,  # 訂單總金額（不含運費）
            "status": self.status,  # 訂單狀態（如 pending, shipped, completed）
            "shipping_fee": self.shipping_fee,  # 運費金額
            "payment_status": self.payment_status,  # 付款狀態（如 unpaid, paid）
            "remark": self.remark,  # 訂單備註欄，客服或買家可能會填寫說明
            "receiver_name": self.receiver_name,  # 收件人姓名
            "receiver_phone": self.receiver_phone,  # 收件人電話
            "shipping_address": self.shipping_address,  # 收件人地址
            "created_at": self.created_at,  # 訂單建立時間
            "updated_at": self.updated_at,  # 訂單最後更新時間（如變更狀態）
        }

        if include_items:  # 如果參數要求要帶出商品明細
            data["items"] = [item.to_dict() for item in self.items]  # 將所有 OrderItem 關聯的商品逐一轉為字典放入 items 欄位

        if include_history:  # 如果參數要求帶出訂單歷史紀錄（如狀態異動紀錄）
            data["history"] = [h.to_dict() for h in self.histories]  # 將每一筆 OrderHistory 關聯的資料轉為 dict，放入 history 欄位

        if include_user:  # 如果參數要求帶出該訂單所屬的使用者資訊
            data["user"] = self.user.to_dict() if self.user else None  # 若有關聯的 user，就轉為 dict 放入 user 欄位，否則回傳 None

        return data  # 回傳整理好的資料字典



class OrderItem(db.Model):  # 商品明細資料表（子表）
    __tablename__ = 'order_items'  # 對應資料庫中的表名

    id = db.Column(db.Integer, primary_key=True)  # 主鍵
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'), nullable=False)  # 外鍵：對應到訂單
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='RESTRICT'), nullable=False)  # 外鍵：對應到產品
    product_name = db.Column(db.String(120), nullable=False)  # 商品名稱
    qty = db.Column(db.Integer, nullable=False)  # 數量
    price = db.Column(db.Float, nullable=False)  # 價格（單價）
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))  # 建立時間

    def to_dict(self):  # 將明細資料轉成 dict，方便前端用
        return {
            "id": self.id,
            "order_id": self.order_id,
            "product_id": self.product_id,
            "product_name": self.product_name,
            "qty": self.qty,
            "price": self.price,
            "created_at": self.created_at,
        }


class OrderHistory(db.Model):  # 訂單歷史紀錄（例如狀態變更）
    __tablename__ = 'order_histories'  # 對應資料表名稱

    id = db.Column(db.Integer, primary_key=True)  # 主鍵
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'), nullable=False)  # 外鍵：對應訂單
    status = db.Column(db.String(20), nullable=False)  # 訂單狀態（例如：pending、shipped、completed）
    operator = db.Column(db.String(64), nullable=False)  # 操作人（系統或後台人員）
    operated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))  # 操作時間
    remark = db.Column(db.Text)  # 備註說明

    def to_dict(self):  # 轉為 dict 格式
        return {
            "id": self.id,
            "order_id": self.order_id,
            "status": self.status,
            "operator": self.operator,
            "operated_at": self.operated_at,
            "remark": self.remark,
        }
