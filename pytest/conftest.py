# tests/conftest.py
import pytest
import os
from app import create_app, db
from app.models import User, Product, Customer, Order, OrderItem, Category
from werkzeug.security import generate_password_hash
from datetime import datetime

# 設定測試環境變數
os.environ['FLASK_ENV'] = 'testing'

@pytest.fixture(scope="function")
def app():
    """測試用 app fixture"""
    app = create_app()
    
    # 測試專用配置
    app.config.update({
        "TESTING": True,
        "PROPAGATE_EXCEPTIONS": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "JWT_SECRET_KEY": "test-secret-key",
        "SECRET_KEY": "test-secret-key",
        "WTF_CSRF_ENABLED": False,
        # 綠界測試設定
        "ECPAY_MERCHANT_ID": "2000132",
        "ECPAY_HASH_KEY": "5294y06JbISpM5x9",
        "ECPAY_HASH_IV": "v77hoKGq4kWxNNIS",
        "ECPAY_NOTIFY_URL": "http://localhost:5000/payments/ecpay/callback",
        "ECPAY_ORDER_RETURN_URL": "http://localhost:5000/payments/ecpay/return",
        "FRONTEND_URL": "http://localhost:3000"
    })

    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app


@pytest.fixture(scope="function")
def client(app):
    """測試用 client fixture"""
    return app.test_client()


@pytest.fixture
def admin_user(app):
    """管理員使用者"""
    with app.app_context():
        admin = User(
            username="admin",
            email="admin@test.com",
            password_hash=generate_password_hash("admin123"),
            role="admin",
            is_active=True
        )
        db.session.add(admin)
        db.session.commit()
        db.session.refresh(admin)  # 確保 ID 已載入
        return admin


@pytest.fixture
def seller_user(app):
    """銷售人員使用者"""
    with app.app_context():
        seller = User(
            username="seller",
            email="seller@test.com", 
            password_hash=generate_password_hash("seller123"),
            role="seller",
            is_active=True
        )
        db.session.add(seller)
        db.session.commit()
        db.session.refresh(seller)
        return seller


@pytest.fixture
def customer_user(app):
    """客戶使用者"""
    with app.app_context():
        customer = User(
            username="customer",
            email="customer@test.com",
            password_hash=generate_password_hash("customer123"),
            role="customer",
            is_active=True
        )
        db.session.add(customer)
        db.session.commit()
        db.session.refresh(customer)
        return customer


@pytest.fixture
def test_category(app):
    """測試商品分類"""
    with app.app_context():
        category = Category(
            name="測試分類",
            parent_id=None
        )
        db.session.add(category)
        db.session.commit()
        db.session.refresh(category)
        return category


@pytest.fixture
def test_product(app, test_category):
    """測試商品"""
    with app.app_context():
        product = Product(
            name="測試商品",
            desc="測試商品描述",
            price=100.0,
            promo_price=90.0,
            stock=10,
            category_id=test_category.id,
            is_active=True
        )
        db.session.add(product)
        db.session.commit()
        db.session.refresh(product)
        return product


@pytest.fixture
def test_customer(app):
    """測試客戶資料"""
    with app.app_context():
        customer = Customer(
            name="測試客戶",
            email="testcustomer@test.com",
            phone="0912345678",
            address="測試地址",
            tags="VIP,新客戶"
        )
        db.session.add(customer)
        db.session.commit()
        db.session.refresh(customer)
        return customer


@pytest.fixture
def test_order(app, customer_user, test_customer, test_product):
    """測試訂單"""
    with app.app_context():
        # 生成唯一的訂單編號
        order_sn = f"TEST{int(datetime.now().timestamp())}"
        
        order = Order(
            order_sn=order_sn,
            user_id=customer_user.id,
            customer_id=test_customer.id,
            total_amount=100.0,
            shipping_fee=0.0,
            status="pending",
            payment_status="unpaid",
            receiver_name="測試收件人",
            receiver_phone="0912345678",
            shipping_address="測試收件地址"
        )
        db.session.add(order)
        db.session.flush()
        
        # 新增訂單明細
        order_item = OrderItem(
            order_id=order.id,
            product_id=test_product.id,
            product_name=test_product.name,
            qty=1,
            price=test_product.price
        )
        db.session.add(order_item)
        db.session.commit()
        db.session.refresh(order)
        return order


def get_auth_headers(client, email, password):
    """取得認證 headers 的輔助函數"""
    response = client.post('/auth/login', json={
        'email': email,
        'password': password
    })
    if response.status_code == 200:
        token = response.get_json()['access_token']
        return {'Authorization': f'Bearer {token}'}
    return {}


@pytest.fixture
def admin_headers(client, admin_user):
    """管理員認證 headers"""
    return get_auth_headers(client, 'admin@test.com', 'admin123')


@pytest.fixture
def seller_headers(client, seller_user):
    """銷售人員認證 headers"""
    return get_auth_headers(client, 'seller@test.com', 'seller123')


@pytest.fixture
def customer_headers(client, customer_user):
    """客戶認證 headers"""
    return get_auth_headers(client, 'customer@test.com', 'customer123')