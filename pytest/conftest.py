# tests/conftest.py
import pytest  # 匯入 pytest，用於測試框架與 fixture 設定
import os  # 匯入 os 模組，用於操作作業系統功能（例如環境變數）
from app import create_app, db  # 從 app 模組匯入 create_app 工廠函式與資料庫 db 物件
from app.models import User, Product, Customer, Order, OrderItem, Category  # 匯入資料模型：使用者、產品、顧客、訂單、訂單明細、分類
from werkzeug.security import generate_password_hash  # 匯入加密密碼函式
from datetime import datetime  # 匯入日期時間模組，用於產生 timestamp

os.environ['FLASK_ENV'] = 'testing'  # 設定 Flask 環境變數為 testing 模式（避免使用正式資料庫）

@pytest.fixture(scope="function")  # 定義一個 pytest fixture，作用範圍為每個函式呼叫一次
def app():  # 建立測試用的 Flask app
    """測試用 app fixture"""
    app = create_app()  # 呼叫應用工廠函數建立 Flask 實例

    app.config.update({  # 覆蓋原本設定，使用測試專用設定
        "TESTING": True,  # 啟用測試模式（例外會回傳給測試者）
        "PROPAGATE_EXCEPTIONS": True,  # 錯誤向外拋出（便於除錯）
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # 使用記憶體內的 SQLite 資料庫（測試速度快）
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,  # 不追蹤資料庫修改事件（可節省資源）
        "JWT_SECRET_KEY": "test-secret-key",  # 測試用的 JWT 金鑰
        "SECRET_KEY": "test-secret-key",  # Flask session 加密金鑰
        "WTF_CSRF_ENABLED": False,  # 停用 CSRF 檢查（方便測試表單與 POST 請求）
        "ECPAY_MERCHANT_ID": "2000132",  # 綠界測試商店編號
        "ECPAY_HASH_KEY": "5294y06JbISpM5x9",  # 綠界測試金鑰
        "ECPAY_HASH_IV": "v77hoKGq4kWxNNIS",  # 綠界測試 IV
        "ECPAY_NOTIFY_URL": "http://localhost:5000/payments/ecpay/callback",  # 綠界付款完成後 callback 的 API 位址
        "ECPAY_ORDER_RETURN_URL": "http://localhost:5000/payments/ecpay/return",  # 綠界付款成功後的導向 URL
        "FRONTEND_URL": "http://localhost:3000"  # 前端測試用位址
    })

    with app.app_context():  # 啟動應用上下文（必須進入 context 才能操作 db）
        db.drop_all()  # 清空所有資料表（重設資料庫）
        db.create_all()  # 重新建立所有資料表
        yield app  # 將 app 實例傳給測試函式使用（執行完後自動清理）

@pytest.fixture(scope="function")  # 每個測試函式執行一次
def client(app):  # 提供測試用的 HTTP client
    """測試用 client fixture"""
    return app.test_client()  # 回傳 Flask 內建的測試 client，可模擬 HTTP 請求

@pytest.fixture  # 建立管理員帳號
def admin_user(app):
    """管理員使用者"""
    with app.app_context():  # 進入 app context 才能操作資料庫
        admin = User(  # 建立使用者物件
            username="admin",  # 使用者名稱
            email="admin@test.com",  # 使用者信箱
            password_hash=generate_password_hash("admin123"),  # 加密密碼
            role="admin",  # 設定角色為管理員
            is_active=True  # 啟用帳號
        )
        db.session.add(admin)  # 將使用者加到資料庫 session
        db.session.commit()  # 提交 session，將使用者寫入資料庫
        db.session.refresh(admin)  # 重新整理 admin，取得 ID 等資訊
        return admin  # 回傳建立好的管理員物件

@pytest.fixture  # 建立銷售人員帳號
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

@pytest.fixture  # 建立客戶帳號（使用者模型）
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

@pytest.fixture  # 建立商品分類資料
def test_category(app):
    """測試商品分類"""
    with app.app_context():
        category = Category(  # 建立分類
            name="測試分類",  # 分類名稱
            parent_id=None  # 沒有父分類（為根分類）
        )
        db.session.add(category)
        db.session.commit()
        db.session.refresh(category)
        return category

@pytest.fixture  # 建立測試商品
def test_product(app, test_category):  # 依賴 test_category fixture
    """測試商品"""
    with app.app_context():
        product = Product(
            name="測試商品",
            desc="測試商品描述",
            price=100.0,  # 原價
            promo_price=90.0,  # 特價
            stock=10,  # 庫存
            category_id=test_category.id,  # 所屬分類
            is_active=True  # 是否上架
        )
        db.session.add(product)
        db.session.commit()
        db.session.refresh(product)
        return product

@pytest.fixture  # 建立測試用的顧客（非 User，而是 Customer 模型）
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

@pytest.fixture  # 建立測試訂單與訂單明細
def test_order(app, customer_user, test_customer, test_product):
    """測試訂單"""
    with app.app_context():
        order_sn = f"TEST{int(datetime.now().timestamp())}"  # 以 timestamp 建立唯一訂單編號
        order = Order(
            order_sn=order_sn,
            user_id=customer_user.id,  # 建立訂單者
            customer_id=test_customer.id,  # 顧客資料
            total_amount=100.0,
            shipping_fee=0.0,
            status="pending",
            payment_status="unpaid",
            receiver_name="測試收件人",
            receiver_phone="0912345678",
            shipping_address="測試收件地址"
        )
        db.session.add(order)
        db.session.flush()  # 先 flush 讓 order 有 ID 可供使用（尚未 commit）

        order_item = OrderItem(  # 建立訂單明細
            order_id=order.id,
            product_id=test_product.id,
            product_name=test_product.name,
            qty=1,
            price=test_product.price
        )
        db.session.add(order_item)
        db.session.commit()  # 一次提交訂單與明細
        db.session.refresh(order)  # 重新讀取資料以確保同步
        return order

def get_auth_headers(client, email, password):  # 登入並取得 Bearer token header
    """取得認證 headers 的輔助函數"""
    response = client.post('/auth/login', json={  # 發送 POST 請求登入
        'email': email,
        'password': password
    })
    if response.status_code == 200:  # 若登入成功
        token = response.get_json()['access_token']  # 取得 access_token
        return {'Authorization': f'Bearer {token}'}  # 組成 Bearer token header
    return {}  # 若失敗，回傳空字典

@pytest.fixture  # 管理員用的認證 headers
def admin_headers(client, admin_user):
    """管理員認證 headers"""
    return get_auth_headers(client, 'admin@test.com', 'admin123')

@pytest.fixture  # 銷售人員用的認證 headers
def seller_headers(client, seller_user):
    """銷售人員認證 headers"""
    return get_auth_headers(client, 'seller@test.com', 'seller123')

@pytest.fixture  # 客戶用的認證 headers
def customer_headers(client, customer_user):
    """客戶認證 headers"""
    return get_auth_headers(client, 'customer@test.com', 'customer123')
