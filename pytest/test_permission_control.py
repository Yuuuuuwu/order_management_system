# tests/test_permission_control.py
"""
權限控制測試 - 驗證不同角色的存取權限
"""
import pytest


class TestPermissionControl:
    """權限控制功能測試"""
    
    def test_admin_access_all_users(self, client, admin_headers, customer_user):
        """測試管理員可存取所有使用者"""
        response = client.get('/users', headers=admin_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) >= 1
    
    def test_customer_access_limited_users(self, client, customer_headers):
        """測試客戶只能存取自己的資料"""
        response = client.get('/users', headers=customer_headers)
        assert response.status_code == 200
        data = response.get_json()
        # 客戶應該只能看到自己的資料
        assert 'data' in data
        assert 'total' in data
        assert len(data['data']) == 1
        assert data['data'][0]['role'] == 'customer'
    
    def test_admin_access_all_orders(self, client, admin_headers, test_order):
        """測試管理員可存取所有訂單"""
        response = client.get('/orders', headers=admin_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert 'data' in data
        assert 'total' in data
        assert len(data['data']) >= 1
    
    def test_customer_access_own_orders_only(self, client, customer_headers, test_order):
        """測試客戶只能存取自己的訂單"""
        response = client.get('/orders', headers=customer_headers)
        assert response.status_code == 200
        data = response.get_json()
        # 驗證回傳的訂單都屬於該客戶
        assert 'data' in data
        for order in data['data']:
            assert order['user_id'] == test_order.user_id
    
    def test_customer_cannot_access_other_order(self, client, admin_user, test_order, app):
        """測試客戶無法存取其他人的訂單"""
        # 建立另一個客戶並登入
        with app.app_context():
            from app.models import User
            from werkzeug.security import generate_password_hash
            from app import db
            import uuid
            
            # 使用唯一的用戶名避免衝突
            unique_username = f"othercustomer_{uuid.uuid4().hex[:8]}"
            unique_email = f"other_{uuid.uuid4().hex[:8]}@test.com"
            
            other_customer = User(
                username=unique_username,
                email=unique_email,
                password_hash=generate_password_hash("password123"),
                role="customer"
            )
            db.session.add(other_customer)
            db.session.commit()
        
        # 其他客戶登入
        login_response = client.post('/auth/login', json={
            'username': unique_username,
            'password': 'password123'
        })
        assert login_response.status_code == 200
        login_data = login_response.get_json()
        assert 'access_token' in login_data
        other_headers = {'Authorization': f'Bearer {login_data["access_token"]}'}
        
        # 嘗試存取不屬於自己的訂單
        response = client.get(f'/orders/{test_order.id}', headers=other_headers)
        assert response.status_code == 403
    
    def test_customer_cannot_update_order_status(self, client, customer_headers, test_order):
        """測試客戶無法更新訂單狀態"""
        response = client.put(f'/orders/{test_order.id}', 
                             headers=customer_headers, json={
            'status': 'shipped'
        })
        assert response.status_code == 403
    
    def test_admin_can_update_order_status(self, client, admin_headers, test_order):
        """測試管理員可以更新訂單狀態"""
        response = client.put(f'/orders/{test_order.id}', 
                             headers=admin_headers, json={
            'status': 'shipped',
            'remark': '管理員更新'
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'shipped'
    
    def test_customer_cannot_create_product(self, client, customer_headers):
        """測試客戶無法建立商品"""
        response = client.post('/products', headers=customer_headers, json={
            'name': '測試商品',
            'price': 100.0
        })
        assert response.status_code == 403
    
    def test_seller_can_create_product(self, client, seller_headers, test_category):
        """測試銷售人員可以建立商品"""
        response = client.post('/products', headers=seller_headers, json={
            'name': '銷售員商品',
            'desc': '銷售員建立的商品',
            'price': 150.0,
            'stock': 5,
            'category_id': test_category.id,
            'is_active': True
        })
        assert response.status_code == 201
        data = response.get_json()
        assert data['name'] == '銷售員商品'
    
    def test_customer_cannot_access_admin_dashboard(self, client, customer_headers):
        """測試客戶無法存取管理儀表板"""
        response = client.get('/dashboard/summary', headers=customer_headers)
        assert response.status_code == 403
    
    def test_admin_can_access_dashboard(self, client, admin_headers):
        """測試管理員可以存取儀表板"""
        response = client.get('/dashboard/summary', headers=admin_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert 'order_count' in data or 'total_sales' in data
    
    def test_unauthenticated_cannot_access_protected_routes(self, client):
        """測試未認證使用者無法存取受保護路由"""
        protected_routes = [
            '/orders',
            '/payments',
            '/users',
            '/dashboard/summary'
        ]
        
        for route in protected_routes:
            response = client.get(route)
            assert response.status_code == 401