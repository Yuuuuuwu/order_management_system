# tests/test_integration_flow.py
"""
整合測試 - 測試完整的業務流程
"""
import pytest


class TestIntegrationFlow:
    """完整業務流程整合測試"""
    
    def test_complete_ecommerce_flow(self, client, app):
        """測試完整的電商流程：註冊→建立商品→下單→付款"""
        
        # 1. 註冊管理員
        admin_response = client.post('/auth/register', json={
            'username': 'flowadmin',
            'email': 'admin@flow.com',
            'password': 'admin123',
            'role': 'admin'
        })
        assert admin_response.status_code == 201
        
        # 2. 管理員登入
        admin_login = client.post('/auth/login', json={
            'username': 'flowadmin',
            'password': 'admin123'
        })
        assert admin_login.status_code == 200
        admin_token = admin_login.get_json()['access_token']
        admin_headers = {'Authorization': f'Bearer {admin_token}'}
        
        # 3. 建立商品分類
        category_response = client.post('/categories', 
                                       headers=admin_headers, json={
            'name': '整合測試分類'
        })
        assert category_response.status_code == 201
        category_id = category_response.get_json()['id']
        
        # 4. 建立商品
        product_response = client.post('/products', 
                                      headers=admin_headers, json={
            'name': '整合測試商品',
            'desc': '用於整合測試的商品',
            'price': 299.0,
            'stock': 100,
            'category_id': category_id,
            'is_active': True
        })
        assert product_response.status_code == 201
        product = product_response.get_json()
        
        # 5. 建立客戶資料
        customer_response = client.post('/customers', json={
            'name': '整合測試客戶',
            'email': 'customer@flow.com',
            'phone': '0912345678',
            'address': '整合測試地址'
        })
        assert customer_response.status_code == 201
        customer = customer_response.get_json()
        
        # 6. 註冊一般客戶使用者
        user_response = client.post('/auth/register', json={
            'username': 'flowcustomer',
            'email': 'user@flow.com',
            'password': 'user123',
            'role': 'customer'
        })
        assert user_response.status_code == 201
        
        # 7. 客戶登入
        user_login = client.post('/auth/login', json={
            'username': 'flowcustomer',
            'password': 'user123'
        })
        assert user_login.status_code == 200
        user_token = user_login.get_json()['access_token']
        user_headers = {'Authorization': f'Bearer {user_token}'}
        
        # 8. 客戶建立訂單
        order_response = client.post('/orders', 
                                    headers=user_headers, json={
            'customer_id': customer['id'],
            'items': [
                {
                    'product_id': product['id'],
                    'qty': 2
                }
            ],
            'receiver_name': '整合測試收件人',
            'receiver_phone': '0912345678',
            'shipping_address': '整合測試收件地址',
            'remark': '整合測試訂單'
        })
        assert order_response.status_code == 201
        order = order_response.get_json()
        assert order['total_amount'] == 598.0  # 299 * 2
        
        # 9. 客戶進行付款
        payment_response = client.post(f'/payments/{order["id"]}', 
                                      headers=user_headers)
        assert payment_response.status_code == 201
        payment = payment_response.get_json()
        assert payment['status'] == 'success'
        
        # 10. 驗證訂單狀態已更新
        order_check = client.get(f'/orders/{order["id"]}', 
                                headers=user_headers)
        assert order_check.status_code == 200
        updated_order = order_check.get_json()
        assert updated_order['status'] == 'paid'
        
        # 11. 管理員查看訂單
        admin_order_check = client.get(f'/orders/{order["id"]}', 
                                      headers=admin_headers)
        assert admin_order_check.status_code == 200
        
        # 12. 管理員更新訂單狀態為已出貨
        ship_response = client.put(f'/orders/{order["id"]}', 
                                  headers=admin_headers, json={
            'status': 'shipped',
            'remark': '商品已出貨'
        })
        assert ship_response.status_code == 200
        
        # 13. 驗證最終狀態
        final_order = client.get(f'/orders/{order["id"]}', 
                                headers=user_headers)
        final_data = final_order.get_json()
        assert final_data['status'] == 'shipped'
    
    def test_ecpay_payment_integration(self, client, customer_headers, test_order):
        """測試綠界支付完整流程"""
        
        # 1. 產生綠界付款表單
        ecpay_response = client.post(f'/payments/ecpay/{test_order.id}', 
                                    headers=customer_headers)
        assert ecpay_response.status_code == 200
        ecpay_data = ecpay_response.get_json()
        trade_no = ecpay_data['params']['MerchantTradeNo']
        
        # 2. 模擬綠界付款成功回調
        from unittest.mock import patch
        callback_data = {
            'MerchantTradeNo': trade_no,
            'RtnCode': '1',
            'RtnMsg': '交易成功',
            'TradeAmt': str(int(test_order.total_amount)),
            'CheckMacValue': 'test_mac'
        }
        
        with patch('app.utils.check_mac_value.verify_check_mac_value') as mock_verify:
            mock_verify.return_value = True
            
            callback_response = client.post('/payments/ecpay/callback', 
                                           data=callback_data)
            assert callback_response.status_code == 200
            assert callback_response.get_data(as_text=True) == '1|OK'
        
        # 3. 驗證訂單狀態已更新
        order_check = client.get(f'/orders/{test_order.id}', 
                                headers=customer_headers)
        order_data = order_check.get_json()
        assert order_data['status'] == 'paid'
        
        # 4. 驗證付款記錄已建立
        payments_response = client.get('/payments', headers=customer_headers)
        payments = payments_response.get_json() 
        ecpay_payment = next((p for p in payments if p['payment_method'] == 'ecpay'), None)
        assert ecpay_payment is not None
        assert ecpay_payment['status'] == 'success'
    
    def test_inventory_management_flow(self, client, admin_headers, test_product):
        """測試庫存管理流程"""
        
        # 1. 檢查初始庫存
        product_response = client.get(f'/products/{test_product.id}')
        initial_stock = product_response.get_json()['stock']
        assert initial_stock == 10
        
        # 2. 調整庫存 - 增加
        stock_add = client.put(f'/products/{test_product.id}/stock', 
                              headers=admin_headers, json={
            'stock_change': 5,
            'reason': '進貨'
        })
        assert stock_add.status_code == 200
        assert stock_add.get_json()['stock'] == 15
        
        # 3. 調整庫存 - 減少
        stock_reduce = client.put(f'/products/{test_product.id}/stock', 
                                 headers=admin_headers, json={
            'stock_change': -3,
            'reason': '損耗'
        })
        assert stock_reduce.status_code == 200
        assert stock_reduce.get_json()['stock'] == 12
        
        # 4. 批次停用商品
        batch_disable = client.put('/products/batch/active', 
                                  headers=admin_headers, json={
            'product_ids': [test_product.id],
            'is_active': False
        })
        assert batch_disable.status_code == 200
        
        # 5. 驗證商品已停用
        disabled_check = client.get(f'/products/{test_product.id}')
        assert disabled_check.get_json()['is_active'] == False