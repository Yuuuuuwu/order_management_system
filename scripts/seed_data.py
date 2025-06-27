#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
預設資料載入腳本

載入系統初始化所需的預設資料，包括：
- 預設使用者帳號
- 商品分類和商品資料
- 範例訂單資料
- 客戶資料
- 測試支付記錄

使用方式：
    python scripts/seed_data.py
    
環境變數：
    - FLASK_APP: Flask 應用程式入口
    - DATABASE_URL: 資料庫連接字串
    
Author: OMS Team
Created: 2025-06-25
"""

import sys
import os
from datetime import datetime, timedelta
from decimal import Decimal
from werkzeug.security import generate_password_hash
import random
from faker import Faker

# 添加專案根目錄到 Python 路徑
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.user import User
from app.models.product import Product, Category
from app.models.customer import Customer
from app.models.order import Order, OrderItem
from app.models.payment import Payment
from app.models.notification import Notification

# 初始化 Faker（繁體中文）
fake = Faker('zh_TW')

def init_app():
    """
    初始化 Flask 應用程式
    """
    app = create_app()
    app.app_context().push()
    return app

def create_default_users():
    """
    建立預設使用者帳號
    """
    print("📝 建立預設使用者帳號...")
    
    users_data = [
        {
            'email': 'admin@example.com',
            'name': '系統管理員',
            'role': 'admin',
            'password': 'AdminPassword123!',
            'phone': '02-12345678',
            'is_active': True,
            'email_verified': True
        },
        {
            'email': 'seller@example.com',
            'name': '賣家測試',
            'role': 'seller',
            'password': 'SellerPassword123!',
            'phone': '0912-345-678',
            'is_active': True,
            'email_verified': True
        },
        {
            'email': 'customer@example.com',
            'name': '客戶測試',
            'role': 'customer',
            'password': 'CustomerPassword123!',
            'phone': '0987-654-321',
            'is_active': True,
            'email_verified': True
        }
    ]
    
    created_users = []
    
    for user_data in users_data:
        # 檢查使用者是否已存在
        existing_user = User.query.filter_by(email=user_data['email']).first()
        if existing_user:
            print(f"  ⚠️ 使用者 {user_data['email']} 已存在，跳過建立")
            created_users.append(existing_user)
            continue
            
        # 建立新使用者
        user = User(
            email=user_data['email'],
            username=user_data['name'],
            role=user_data['role'],
            phone=user_data.get('phone'),
            is_active=user_data.get('is_active', True)
        )
        user.set_password(user_data['password'])
        
        db.session.add(user)
        created_users.append(user)
        print(f"  ✅ 建立使用者: {user.email} ({user.role})")
    
    db.session.commit()
    print(f"✅ 完成建立 {len(created_users)} 個使用者帳號")
    return created_users

def create_categories():
    """
    建立商品分類
    """
    print("\n📝 建立商品分類...")
    
    categories_data = [
        {'name': '手機', 'description': '智慧型手機及相關配件'},
        {'name': '筆電', 'description': '筆記型電腦及週邊設備'},
        {'name': '平板', 'description': '平板電腦及配件'},
        {'name': '耳機', 'description': '有線及無線耳機'},
        {'name': '穿戴裝置', 'description': '智慧手錶及健身追蹤器'},
        {'name': '電腦週邊', 'description': '滑鼠、鍵盤、螢幕等週邊設備'},
        {'name': '遊戲', 'description': '遊戲主機及遊戲軟體'},
        {'name': '家電', 'description': '小家電及智慧家電'}
    ]
    
    created_categories = []
    
    for cat_data in categories_data:
        # 檢查分類是否已存在
        existing_cat = Category.query.filter_by(name=cat_data['name']).first()
        if existing_cat:
            print(f"  ⚠️ 分類 {cat_data['name']} 已存在，跳過建立")
            created_categories.append(existing_cat)
            continue
            
        # 建立新分類
        category = Category(
            name=cat_data['name']
        )
        
        db.session.add(category)
        created_categories.append(category)
        print(f"  ✅ 建立分類: {category.name}")
    
    db.session.commit()
    print(f"✅ 完成建立 {len(created_categories)} 個商品分類")
    return created_categories

def create_products(categories):
    """
    建立商品資料
    """
    print("\n📝 建立商品資料...")
    
    products_data = [
        # 手機類
        {
            'name': 'iPhone 15 Pro',
            'description': '6.1吋 Super Retina XDR 顯示器，A17 Pro 晶片，三鏡頭相機系統',
            'sku': 'IPH15PRO001',
            'price': Decimal('35900.00'),
            'stock_quantity': 50,
            'category_name': '手機'
        },
        {
            'name': 'Samsung Galaxy S24 Ultra',
            'description': '6.8吋 Dynamic AMOLED 2X 顯示器，Snapdragon 8 Gen 3，S Pen 支援',
            'sku': 'SAM-S24U-001',
            'price': Decimal('42900.00'),
            'stock_quantity': 30,
            'category_name': '手機'
        },
        
        # 筆電類
        {
            'name': 'MacBook Pro 14吋',
            'description': 'M3 晶片，16GB 記憶體，512GB SSD，14.2吋 Liquid Retina XDR 顯示器',
            'sku': 'MBP14-M3-512',
            'price': Decimal('72900.00'),
            'stock_quantity': 25,
            'category_name': '筆電'
        },
        {
            'name': 'Dell XPS 13',
            'description': 'Intel Core i7，16GB RAM，512GB SSD，13.4吋 InfinityEdge 顯示器',
            'sku': 'DELL-XPS13-I7',
            'price': Decimal('45900.00'),
            'stock_quantity': 20,
            'category_name': '筆電'
        },
        
        # 平板類
        {
            'name': 'iPad Air',
            'description': '10.9吋 Liquid Retina 顯示器，M1 晶片，256GB，支援 Apple Pencil',
            'sku': 'IPAD-AIR-256',
            'price': Decimal('19900.00'),
            'stock_quantity': 40,
            'category_name': '平板'
        },
        
        # 耳機類
        {
            'name': 'AirPods Pro (第 2 代)',
            'description': '主動式降噪，空間音訊，MagSafe 充電盒，最長 6 小時聆聽時間',
            'sku': 'APP-PRO2-001',
            'price': Decimal('7490.00'),
            'stock_quantity': 100,
            'category_name': '耳機'
        },
        {
            'name': 'Sony WH-1000XM5',
            'description': '業界領先的降噪技術，30小時電池續航，快速充電',
            'sku': 'SONY-WH1000XM5',
            'price': Decimal('11900.00'),
            'stock_quantity': 35,
            'category_name': '耳機'
        },
        
        # 穿戴裝置類
        {
            'name': 'Apple Watch Series 9',
            'description': '45mm GPS，鋁金屬錶殼，運動型錶帶，健康監測功能',
            'sku': 'AW-S9-45-GPS',
            'price': Decimal('12900.00'),
            'stock_quantity': 60,
            'category_name': '穿戴裝置'
        },
        
        # 電腦週邊類
        {
            'name': 'Magic Keyboard',
            'description': '無線鍵盤，背光按鍵，內建充電電池，支援 Touch ID',
            'sku': 'MK-TOUCH-001',
            'price': Decimal('4390.00'),
            'stock_quantity': 75,
            'category_name': '電腦週邊'
        },
        {
            'name': 'Logitech MX Master 3S',
            'description': '無線滑鼠，MagSpeed 滾輪，多裝置連接，70天電池續航',
            'sku': 'LOG-MXM3S-001',
            'price': Decimal('3290.00'),
            'stock_quantity': 45,
            'category_name': '電腦週邊'
        }
    ]
    
    # 建立分類映射
    category_map = {cat.name: cat for cat in categories}
    
    created_products = []
    
    for prod_data in products_data:
        # 檢查商品是否已存在
        existing_product = Product.query.filter_by(name=prod_data['name']).first()
        if existing_product:
            print(f"  ⚠️ 商品 {prod_data['name']} 已存在，跳過建立")
            created_products.append(existing_product)
            continue
            
        # 獲取分類
        category = category_map.get(prod_data['category_name'])
        if not category:
            print(f"  ❌ 找不到分類: {prod_data['category_name']}")
            continue
            
        # 建立新商品
        product = Product(
            name=prod_data['name'],
            desc=prod_data['description'],
            price=prod_data['price'],
            stock=prod_data['stock_quantity'],
            category_id=category.id,
            is_active=True
        )
        
        db.session.add(product)
        created_products.append(product)
        print(f"  ✅ 建立商品: {product.name} (NT${product.price})")
    
    db.session.commit()
    print(f"✅ 完成建立 {len(created_products)} 個商品")
    return created_products

def create_customers():
    """
    建立客戶資料
    """
    print("\n📝 建立客戶資料...")
    
    created_customers = []
    
    # 建立預設客戶
    default_customers = [
        {
            'name': '王小明',
            'email': 'wang.xiaoming@example.com',
            'phone': '0912-345-678',
            'address': '台北市信義區信義路五段7號'
        },
        {
            'name': '李美華',
            'email': 'li.meihua@example.com', 
            'phone': '0987-654-321',
            'address': '新北市板橋區中山路一段161號'
        },
        {
            'name': '陳志豪',
            'email': 'chen.zhihao@example.com',
            'phone': '0956-789-012',
            'address': '台中市西屯區台灣大道三段99號'
        }
    ]
    
    # 建立預設客戶
    for cust_data in default_customers:
        existing_customer = Customer.query.filter_by(email=cust_data['email']).first()
        if existing_customer:
            print(f"  ⚠️ 客戶 {cust_data['email']} 已存在，跳過建立")
            created_customers.append(existing_customer)
            continue
            
        customer = Customer(
            name=cust_data['name'],
            email=cust_data['email'],
            phone=cust_data['phone'],
            address=cust_data['address']
        )
        
        db.session.add(customer)
        created_customers.append(customer)
        print(f"  ✅ 建立客戶: {customer.name}")
    
    # 建立隨機客戶資料
    for i in range(15):
        email = fake.email()
        
        # 檢查email是否重複
        if Customer.query.filter_by(email=email).first():
            continue
            
        customer = Customer(
            name=fake.name(),
            email=email,
            phone=fake.phone_number(),
            address=fake.address()
        )
        
        db.session.add(customer)
        created_customers.append(customer)
        
        if (i + 1) % 5 == 0:
            print(f"  ✅ 已建立 {i + 1} 個隨機客戶")
    
    db.session.commit()
    print(f"✅ 完成建立 {len(created_customers)} 個客戶")
    return created_customers

def create_orders(customers, products, users):
    """
    建立訂單資料
    """
    print("\n📝 建立訂單資料...")
    
    # 找到客戶角色的使用者
    customer_user = next((u for u in users if u.role == 'customer'), None)
    if not customer_user:
        print("  ❌ 找不到客戶角色的使用者")
        return []
    
    created_orders = []
    order_statuses = ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']
    payment_methods = ['credit_card', 'bank_transfer', 'cash_on_delivery']
    
    # 建立最近 3 個月的訂單
    for i in range(25):
        # 隨機選擇客戶
        customer = random.choice(customers)
        
        # 隨機選擇 1-4 個商品
        order_products = random.sample(products, random.randint(1, 4))
        
        # 計算訂單總金額
        total_amount = Decimal('0.00')
        order_items = []
        
        for product in order_products:
            quantity = random.randint(1, 3)
            price = Decimal(str(product.price))
            subtotal = price * quantity
            total_amount += subtotal
            
            order_items.append({
                'product': product,
                'quantity': quantity,
                'price': price,
                'subtotal': subtotal
            })
        
        # 建立訂單
        order_date = datetime.utcnow() - timedelta(days=random.randint(1, 90))
        order_sn = f"ORD{order_date.strftime('%Y%m%d')}{str(i+1).zfill(3)}"
        
        order = Order(
            order_sn=order_sn,
            user_id=customer_user.id,
            customer_id=customer.id,
            status=random.choice(order_statuses),
            total_amount=float(total_amount),
            shipping_address=customer.address or fake.address(),
            receiver_name=customer.name,
            receiver_phone=customer.phone or fake.phone_number(),
            remark=fake.text(max_nb_chars=100) if random.choice([True, False]) else None
        )
        
        db.session.add(order)
        db.session.flush()  # 取得 order.id
        
        # 建立訂單項目
        for item_data in order_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item_data['product'].id,
                product_name=item_data['product'].name,
                qty=item_data['quantity'],
                price=float(item_data['price'])
            )
            db.session.add(order_item)
        
        # 建立支付記錄（某些訂單）
        if order.status in ['confirmed', 'shipped', 'delivered'] or random.choice([True, False]):
            payment_status = 'success' if order.status in ['confirmed', 'shipped', 'delivered'] else random.choice(['pending', 'failed', 'completed'])
            
            payment = Payment(
                order_id=order.id,
                payment_method=random.choice(payment_methods),
                amount=float(total_amount),
                status=payment_status,
                transaction_id=f"TXN{order_date.strftime('%Y%m%d')}{random.randint(100000, 999999)}"
            )
            db.session.add(payment)
        
        created_orders.append(order)
        
        if (i + 1) % 5 == 0:
            print(f"  ✅ 已建立 {i + 1} 個訂單")
    
    db.session.commit()
    print(f"✅ 完成建立 {len(created_orders)} 個訂單")
    return created_orders

def create_notifications(users, orders):
    """
    建立通知資料
    """
    print("\n📝 建立通知資料...")
    
    created_notifications = []
    notification_types = ['order', 'payment', 'system', 'promotion']
    
    # 為每個使用者建立一些通知
    for user in users:
        # 建立 3-8 個通知
        for i in range(random.randint(3, 8)):
            notification_type = random.choice(notification_types)
            
            # 根據類型生成不同的通知內容
            if notification_type == 'order':
                if orders:
                    order = random.choice(orders)
                    title = f"訂單 {order.order_sn} 狀態更新"
                    content = f"您的訂單狀態已更新為：{order.status}"
                else:
                    title = "訂單狀態更新"
                    content = "您有新的訂單狀態更新"
            elif notification_type == 'payment':
                title = "支付完成通知"
                content = "您的支付已成功處理，感謝您的購買！"
            elif notification_type == 'system':
                title = "系統維護通知"
                content = "系統將於今晚 23:00-24:00 進行維護，期間可能影響服務使用。"
            else:  # promotion
                title = "限時優惠活動"
                content = "新品上市特價中！立即購買享受85折優惠，優惠有限期，把握機會！"
            
            notification = Notification(
                user_id=user.id,
                type=notification_type,
                title=title,
                content=content,
                is_read=random.choice([True, False]),
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30))
            )
            
            db.session.add(notification)
            created_notifications.append(notification)
    
    db.session.commit()
    print(f"✅ 完成建立 {len(created_notifications)} 個通知")
    return created_notifications

def main():
    """
    主要執行函數
    """
    print("🚀 開始載入預設資料...")
    print("=" * 50)
    
    try:
        # 初始化應用程式
        app = init_app()
        
        # 確保資料庫表格存在
        db.create_all()
        
        # 依序建立資料
        users = create_default_users()
        categories = create_categories()
        products = create_products(categories)
        customers = create_customers()
        orders = create_orders(customers, products, users)
        notifications = create_notifications(users, orders)
        
        print("\n" + "=" * 50)
        print("🎉 預設資料載入完成！")
        print("\n📊 載入統計：")
        print(f"  👥 使用者帳號: {len(users)} 個")
        print(f"  📂 商品分類: {len(categories)} 個")
        print(f"  📦 商品資料: {len(products)} 個")
        print(f"  🏪 客戶資料: {len(customers)} 個")
        print(f"  📋 訂單資料: {len(orders)} 個")
        print(f"  🔔 通知資料: {len(notifications)} 個")
        
        print("\n🔑 預設登入帳號：")
        print("  管理員: admin@example.com / AdminPassword123!")
        print("  賣家: seller@example.com / SellerPassword123!")
        print("  客戶: customer@example.com / CustomerPassword123!")
        
        print("\n🌐 存取網址：")
        print("  前端: http://localhost:5173")
        print("  後端 API: http://localhost:5000")
        print("  API 文件: http://localhost:5000/api/v1/docs/")
        
    except Exception as e:
        print(f"\n❌ 載入預設資料時發生錯誤: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()