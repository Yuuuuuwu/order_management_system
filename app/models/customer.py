from app import db
from sqlalchemy.orm import relationship
from datetime import datetime

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.String(32))
    address = db.Column(db.String(128))
    email = db.Column(db.String(64))
    tags = db.Column(db.String(128))  # 逗號分隔標籤，如 VIP,一級客戶
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    orders = relationship('Order', back_populates='customer')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'address': self.address,
            'email': self.email,
            'tags': self.tags.split(',') if self.tags else [],
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
