# tests/test_payment_flow.py
"""
付款流程測試 - 包含模擬付款和綠界支付
"""
import pytest
from unittest.mock import patch


class TestPaymentFlow:
    """付款流程功能測試"""
    
    def test_mock_payment_success(self, client, customer_headers, test_order):
        """測試模擬付款成功"""
        response = client.post(f'/payments/{test_order.id}', 
                              headers=customer_headers)
        assert response.status_code == 201
        data = response.get_json()
        assert data['status'] == 'success'
        assert data['payment_method'] == 'mock'
        assert data['order_id'] == test_order.id
        assert data['amount'] == test_order.total_amount
    
    def test_payment_already_paid_order(self, client, customer_headers, test_order, app):
        """測試付款已付款的訂單"""
        # 先將訂單設為已付款
        with app.app_context():
            from app import db
            from app.models import Order
            order = Order.query.get(test_order.id)
            order.status = 'paid'
            db.session.commit()
        
        response = client.post(f'/payments/{test_order.id}', 
                              headers=customer_headers)
        assert response.status_code == 400
        data = response.get_json()
        assert '已付款或已取消' in data.get('message', data.get('description', ''))
    
    def test_payment_nonexistent_order(self, client, customer_headers):
        """測試付款不存在的訂單"""
        response = client.post('/payments/99999', headers=customer_headers)
        assert response.status_code == 404
    
    def test_ecpay_payment_form_generation(self, client, customer_headers, test_order):
        """測試綠界付款表單產生"""
        response = client.post(f'/payments/ecpay/{test_order.id}', 
                              headers=customer_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert 'ecpay_url' in data
        assert 'params' in data
        
        params = data['params']
        assert params['MerchantID'] == '2000132'
        assert 'MerchantTradeNo' in params
        assert 'CheckMacValue' in params
        assert int(params['TotalAmount']) == int(test_order.total_amount)
    
    def test_ecpay_callback_success(self, client, test_order):
        """測試綠界付款成功回調"""
        # 確保訂單有 trade_no
        with client.application.app_context():
            from app.models import Order
            from app import db
            order = Order.query.get(test_order.id)
            if not order.trade_no:
                order.trade_no = f"TEST{order.id}123456"
                db.session.commit()
                test_order.trade_no = order.trade_no  # 更新測試對象
        
        callback_data = {
            'MerchantTradeNo': test_order.trade_no,
            'RtnCode': '1',
            'RtnMsg': '交易成功',
            'TradeAmt': str(int(test_order.total_amount)),
            'CheckMacValue': 'dummy_mac'
        }
        
        with patch('app.routes.payments.verify_check_mac_value') as mock_verify:
            mock_verify.return_value = True
            
            response = client.post('/payments/ecpay/callback', data=callback_data)
            assert response.status_code == 200
            assert response.get_data(as_text=True) == '1|OK'
    
    def test_ecpay_callback_failure(self, client, test_order):
        """測試綠界付款失敗回調"""
        callback_data = {
            'MerchantTradeNo': test_order.trade_no or 'TEST001',
            'RtnCode': '0',
            'RtnMsg': '交易失敗',
            'CheckMacValue': 'dummy_mac'
        }
        
        with patch('app.routes.payments.verify_check_mac_value') as mock_verify:
            mock_verify.return_value = True
            
            response = client.post('/payments/ecpay/callback', data=callback_data)
            assert response.status_code == 200
            assert response.get_data(as_text=True) == '0|FAIL'
    
    def test_ecpay_return_redirect(self, client, test_order):
        """測試綠界付款導回"""
        return_data = {
            'MerchantTradeNo': test_order.trade_no or 'TEST001',
            'RtnCode': '1',
            'RtnMsg': '交易成功'
        }
        
        response = client.post('/payments/ecpay/return', data=return_data)
        assert response.status_code == 302  # 重導狀態碼
        assert 'payment_result' in response.location
    
    def test_get_payment_records_customer(self, client, customer_headers, test_order):
        """測試客戶取得付款記錄"""
        # 先建立一筆付款記錄
        client.post(f'/payments/{test_order.id}', headers=customer_headers)
        
        response = client.get('/payments', headers=customer_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) >= 1
        payment = data[0]
        assert payment['status'] == 'success'
        assert payment['order_id'] == test_order.id
    
    def test_get_payment_records_admin(self, client, admin_headers):
        """測試管理員取得所有付款記錄"""
        response = client.get('/payments', headers=admin_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
    
    def test_get_payment_detail(self, client, customer_headers, test_order):
        """測試取得付款詳情"""
        # 先建立付款記錄
        payment_response = client.post(f'/payments/{test_order.id}', 
                                     headers=customer_headers)
        payment_id = payment_response.get_json()['id']
        
        response = client.get(f'/payments/{payment_id}', 
                             headers=customer_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert data['id'] == payment_id
        assert data['order_id'] == test_order.id