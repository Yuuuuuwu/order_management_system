from app import db
from datetime import datetime
from app.models.user import User  # 確保有 import User 模型

class Order(db.Model):
    """訂單資料表"""
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    order_sn = db.Column(db.String(64), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=True)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending', nullable=False)
    shipping_fee = db.Column(db.Float, default=0, nullable=False)
    payment_status = db.Column(db.String(20), default='unpaid', nullable=False)
    remark = db.Column(db.Text)
    receiver_name = db.Column(db.String(120), nullable=False)
    receiver_phone = db.Column(db.String(40), nullable=False)
    shipping_address = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # 關聯設定
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade="all, delete-orphan")
    histories = db.relationship('OrderHistory', backref='order', lazy=True, cascade="all, delete-orphan")
    customer = db.relationship('Customer', back_populates='orders')
    user = db.relationship('User', backref='orders', lazy=True)  # 加入 user 關聯

    def to_dict(self, include_items=False, include_history=False, include_user=False):
        """轉換為 dict，可選擇是否包含明細、歷史、使用者資料"""
        data = {
            "id": self.id,
            "order_sn": self.order_sn,
            "user_id": self.user_id,
            "customer_id": self.customer_id,
            "total_amount": self.total_amount,
            "status": self.status,
            "shipping_fee": self.shipping_fee,
            "payment_status": self.payment_status,
            "remark": self.remark,
            "receiver_name": self.receiver_name,
            "receiver_phone": self.receiver_phone,
            "shipping_address": self.shipping_address,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
        if include_items:
            data["items"] = [item.to_dict() for item in self.items]
        if include_history:
            data["history"] = [h.to_dict() for h in self.histories]
        if include_user:
            data["user"] = self.user.to_dict() if self.user else None
        return data

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product_name = db.Column(db.String(120), nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "product_id": self.product_id,
            "product_name": self.product_name,
            "qty": self.qty,
            "price": self.price,
            "created_at": self.created_at,
        }

class OrderHistory(db.Model):
    __tablename__ = 'order_histories'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    operator = db.Column(db.String(64), nullable=False)
    operated_at = db.Column(db.DateTime, default=datetime.utcnow)
    remark = db.Column(db.Text)

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "status": self.status,
            "operator": self.operator,
            "operated_at": self.operated_at,
            "remark": self.remark,
        }
