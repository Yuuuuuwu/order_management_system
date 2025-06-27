from app import db
from datetime import datetime

class Category(db.Model):
    """商品分類（支援多層級）"""
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    sku = db.Column(db.String(64), unique=True, nullable=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    parent = db.relationship('Category', remote_side=[id], backref='children')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def to_dict(self, include_children=False):
        data = {
            "id": self.id,
            "name": self.name,
            "parent_id": self.parent_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
        if include_children:
            data["children"] = [c.to_dict() for c in self.children]
        return data

class Product(db.Model):
    """商品資料表"""
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    promo_price = db.Column(db.Float)  # 促銷價，可為 None
    stock = db.Column(db.Integer, default=0)
    desc = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Category', backref='products')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "promo_price": self.promo_price,
            "stock": self.stock,
            "desc": self.desc,
            "image_url": self.image_url,
            "is_active": self.is_active,
            "category_id": self.category_id,
            "category": self.category.to_dict() if self.category else None,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def change_stock(self, delta):
        """庫存異動（正數進貨，負數銷售）"""
        self.stock += delta
        if self.stock < 0:
            self.stock = 0
