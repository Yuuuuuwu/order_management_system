from app import db
from datetime import datetime

class Payment(db.Model):
    """付款資訊資料表"""
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='initiated')  # 可值: initiated, pending, success, failed
    payment_method = db.Column(db.String(40), nullable=False)
    transaction_id = db.Column(db.String(128))
    paid_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
