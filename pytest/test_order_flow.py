# tests/test_order_flow.py
"""
訂單流程測試 - 核心訂單業務邏輯
"""
import pytest


class TestOrderFlow:
    """訂單流程功能測試"""
    
    def test_create_order_success(self, client, customer_headers, test_product, test_customer):
        """測試建立訂單成功"""
        response = client.post('/orders', headers=customer_headers, json={
            'customer_id': test_customer.id,
            'items': [
                {
                    'product_id': test_product.id,
                    'qty': 2
                }
            ],
            'receiver_name': '測試收件人',
            'receiver_phone': '0912345678',
            'shipping_address': '測試收件地址',
            'remark': '測試訂單'
        })
        assert response.status_code == 201
        data = response.get_json()
        assert data['status'] == 'pending'
        assert data['payment_status'] == 'unpaid'
        assert data['total_amount'] == 200.0  # 100 * 2
        assert 'order_sn' in data
        assert len(data['order_sn']) > 0
    
    def test_get_orders_list_customer(self, client, customer_headers, test_order):
        """測試客戶取得自己的訂單列表"""
        response = client.get('/orders', headers=customer_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) >= 1
        order = data[0]
        assert order['status'] == 'pending'
        assert 'order_sn' in order
    
    def test_get_orders_list_admin(self, client, admin_headers, test_order):
        """測試管理員取得所有訂單列表"""
        response = client.get('/orders', headers=admin_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) >= 1
    
    def test_get_order_detail_owner(self, client, customer_headers, test_order):
        """測試訂單擁有者查看訂單詳情"""  
        response = client.get(f'/orders/{test_order.id}', headers=customer_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert data['id'] == test_order.id
        assert data['status'] == 'pending'
        assert 'items' in data
    
    def test_get_order_by_sn(self, client, customer_headers, test_order):
        """測試根據訂單編號查詢訂單"""
        response = client.get(f'/orders/sn/{test_order.order_sn}', 
                             headers=customer_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert data['order_sn'] == test_order.order_sn
    
    def test_update_order_status_admin(self, client, admin_headers, test_order):
        """測試管理員更新訂單狀態"""
        response = client.put(f'/orders/{test_order.id}', 
                             headers=admin_headers, json={
            'status': 'shipped',
            'remark': '已出貨'
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'shipped'
    
    def test_update_order_status_customer_forbidden(self, client, customer_headers, test_order):
        """測試客戶更新訂單狀態被禁止"""
        response = client.put(f'/orders/{test_order.id}', 
                             headers=customer_headers, json={
            'status': 'shipped'
        })
        assert response.status_code == 403
    
    def test_get_order_history(self, client, customer_headers, test_order):
        """測試取得訂單歷史記錄"""
        response = client.get(f'/orders/{test_order.id}/history', 
                             headers=customer_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
    
    def test_batch_update_order_status(self, client, admin_headers, test_order):
        """測試批次更新訂單狀態"""
        response = client.put('/orders/status', 
                             headers=admin_headers, json={
            'order_ids': [test_order.id],
            'status': 'completed',
            'remark': '批次完成'
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data['updated_count'] >= 1
    
    def test_create_order_insufficient_stock(self, client, customer_headers, test_product, test_customer):
        """測試建立訂單庫存不足"""
        response = client.post('/orders', headers=customer_headers, json={
            'customer_id': test_customer.id,
            'items': [
                {
                    'product_id': test_product.id,
                    'qty': 999  # 超過庫存
                }
            ],
            'receiver_name': '測試收件人',
            'receiver_phone': '0912345678',
            'shipping_address': '測試收件地址'
        })
        assert response.status_code == 400