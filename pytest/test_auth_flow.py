# tests/test_auth_flow.py
"""
認證流程測試 - 基於實際專案架構
"""
import pytest


class TestAuthFlow:
    """認證相關功能測試"""
    
    def test_user_registration_success(self, client):
        """測試使用者註冊成功"""
        response = client.post('/auth/register', json={
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password': 'password123',
            'role': 'customer'
        })
        assert response.status_code == 201
        data = response.get_json()
        assert data['username'] == 'newuser'
        assert data['role'] == 'customer'
        assert 'password' not in data
    
    def test_user_registration_missing_role(self, client):
        """測試使用者註冊缺少角色"""
        response = client.post('/auth/register', json={
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password': 'password123'
        })
        assert response.status_code == 400
        data = response.get_json()
        assert '缺少欄位: role' in data.get('message', '')
    
    def test_user_login_success(self, client, customer_user):
        """測試使用者登入成功"""
        response = client.post('/auth/login', json={
            'email': 'customer@test.com',
            'password': 'customer123'
        })
        assert response.status_code == 200
        data = response.get_json()
        assert 'access_token' in data
    
    def test_user_login_wrong_password(self, client, customer_user):
        """測試使用者登入錯誤密碼"""
        response = client.post('/auth/login', json={
            'email': 'customer@test.com',
            'password': 'wrongpassword'
        })
        assert response.status_code == 401
        data = response.get_json()
        assert '帳號或密碼錯誤' in data.get('message', '')
    
    def test_admin_login_success(self, client, admin_user):
        """測試管理員登入成功"""
        response = client.post('/auth/login', json={
            'email': 'admin@test.com',
            'password': 'admin123'
        })
        assert response.status_code == 200
        data = response.get_json()
        assert 'access_token' in data
    
    def test_get_current_user_info(self, client, customer_headers):
        """測試取得當前使用者資訊"""
        response = client.get('/auth/me', headers=customer_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert data['username'] == 'customer'
        assert data['role'] == 'customer'
    
    def test_protected_route_without_token(self, client):
        """測試未登入訪問受保護路由"""
        response = client.get('/auth/me')
        assert response.status_code == 401