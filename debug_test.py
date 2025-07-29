#!/usr/bin/env python3
import os
os.environ['FLASK_ENV'] = 'testing'

from app import create_app, db

app = create_app()
print("App created successfully")
print(f"Config: {app.config['SQLALCHEMY_DATABASE_URI']}")

with app.app_context():
    try:
        db.drop_all()
        db.create_all()
        print("Database tables created successfully")
        
        # 測試基本 API
        with app.test_client() as client:
            # 測試商品列表 API（應該是公開的）
            products_response = client.get('/products')
            print(f"Products response status: {products_response.status_code}")
            print(f"Products response data: {products_response.get_json()}")
            
            # 測試註冊 API
            register_response = client.post('/auth/register', json={
                'username': 'testuser',
                'email': 'test@test.com', 
                'password': 'password123',
                'role': 'customer'
            })
            print(f"Register response status: {register_response.status_code}")
            print(f"Register response data: {register_response.get_json()}")
            
            # 測試登入 API（使用 email）
            login_response = client.post('/auth/login', json={
                'email': 'test@test.com',
                'password': 'password123'
            })
            print(f"Login response status: {login_response.status_code}")
            print(f"Login response data: {login_response.get_json()}")
                
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()