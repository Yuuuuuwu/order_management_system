from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    """
    User (帳號)：可為買家、商家或管理員，用 role 欄位區分
    """
    __tablename__ = 'users'
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(64), unique=True, nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    phone         = db.Column(db.String(40), unique=True, nullable=True)  # 可選填
    role          = db.Column(db.String(20), default="buyer", nullable=False) # "buyer", "seller", "admin"
    is_active     = db.Column(db.Boolean, default=True, nullable=False)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at    = db.Column(db.DateTime, onupdate=datetime.utcnow)
    last_login    = db.Column(db.DateTime)

    stores        = db.relationship('Store', backref='owner', lazy=True)
    orders        = db.relationship('Order', backref='buyer', lazy=True)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

class Store(db.Model):
    """
    Store (商家/店鋪)：用於多商家平台
    """
    __tablename__ = 'stores'
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(128), unique=True, nullable=False)
    owner_id    = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    contact     = db.Column(db.String(64))
    address     = db.Column(db.String(255))
    is_active   = db.Column(db.Boolean, default=True, nullable=False)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at  = db.Column(db.DateTime, onupdate=datetime.utcnow)

    products    = db.relationship('Product', backref='store', lazy=True)

class Product(db.Model):
    """
    Product (商品)
    """
    __tablename__ = 'products'
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(120), nullable=False)
    price       = db.Column(db.Float, nullable=False)
    stock       = db.Column(db.Integer, default=0)
    desc        = db.Column(db.Text)
    image_url   = db.Column(db.String(255))
    is_active   = db.Column(db.Boolean, default=True, nullable=False)
    store_id    = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at  = db.Column(db.DateTime, onupdate=datetime.utcnow)

    order_items = db.relationship('OrderItem', backref='product', lazy=True)

class Order(db.Model):
    """
    Order (訂單)：一筆訂單屬於一位買家
    """
    __tablename__ = 'orders'
    id               = db.Column(db.Integer, primary_key=True)
    order_sn         = db.Column(db.String(64), unique=True, nullable=False) # 訂單編號
    user_id          = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # 買家
    total_amount     = db.Column(db.Float, nullable=False)
    status           = db.Column(db.String(20), default='pending', nullable=False)
    shipping_fee     = db.Column(db.Float, default=0, nullable=False)
    payment_status   = db.Column(db.String(20), default='unpaid', nullable=False)
    remark           = db.Column(db.Text)
    receiver_name    = db.Column(db.String(120), nullable=False)
    receiver_phone   = db.Column(db.String(40), nullable=False)
    shipping_address = db.Column(db.String(255), nullable=False)
    created_at       = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at       = db.Column(db.DateTime, onupdate=datetime.utcnow)

    order_items      = db.relationship('OrderItem', backref='order', lazy=True)
    payment          = db.relationship('Payment', backref='order', uselist=False)

class OrderItem(db.Model):
    """
    OrderItem (訂單明細)：一筆訂單可包含多個商品
    """
    __tablename__ = 'order_items'
    id          = db.Column(db.Integer, primary_key=True)
    order_id    = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id  = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity    = db.Column(db.Integer, nullable=False)
    unit_price  = db.Column(db.Float, nullable=False) # 下單時商品價格
    total_price = db.Column(db.Float, nullable=False) # 單品總價（數量*單價）
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

class Payment(db.Model):
    """
    Payment (付款資訊)：一筆訂單對應一筆付款
    """
    __tablename__ = 'payments'
    id            = db.Column(db.Integer, primary_key=True)
    order_id      = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    amount        = db.Column(db.Float, nullable=False)
    status        = db.Column(db.String(20), default='initiated')
    payment_method= db.Column(db.String(40), nullable=False)    # 如 credit_card, linepay, etc.
    transaction_id= db.Column(db.String(128))   # 第三方支付編號
    paid_at       = db.Column(db.DateTime)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at    = db.Column(db.DateTime, onupdate=datetime.utcnow)