from app import db
from datetime import datetime

class Order(db.Model):
    """訂單資料表"""
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    order_sn = db.Column(db.String(64), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
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
