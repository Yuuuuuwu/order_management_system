# pytest/test_auth_service_unit.py
"""
認證服務單元測試 - 專注測試核心業務邏輯
"""
import pytest
from unittest.mock import Mock, patch
from app.services.auth_service import register_user, authenticate_user


class TestAuthServiceUnit:
    """認證服務單元測試"""
    
    def test_register_user_role_validation(self):
        """測試 register_user 角色驗證邏輯（最重要的業務規則）"""
        # 測試有效角色
        valid_roles = ["admin", "seller", "customer"]
        for role in valid_roles:
            with patch('app.services.auth_service.User') as mock_user_class, \
                 patch('app.services.auth_service.db') as mock_db:
                
                mock_user_instance = Mock()
                mock_user_class.return_value = mock_user_instance
                
                # 應該不拋出異常
                result = register_user("test", "test@test.com", "password", role)
                
                # 驗證 User 被正確初始化
                mock_user_class.assert_called_once_with(
                    username="test", 
                    email="test@test.com", 
                    role=role
                )
                
                # 驗證密碼設定被呼叫
                mock_user_instance.set_password.assert_called_once_with("password")
                
                # 驗證資料庫操作
                mock_db.session.add.assert_called_once_with(mock_user_instance)
                mock_db.session.commit.assert_called_once()
                
                # 驗證回傳值
                assert result == mock_user_instance
    
    def test_register_user_invalid_role_raises_error(self):
        """測試無效角色應拋出 ValueError"""
        invalid_roles = ["invalid", "user", "manager", "", None, 123]
        
        for invalid_role in invalid_roles:
            with pytest.raises(ValueError, match="role 必須是 'admin', 'seller' 或 'customer'"):
                register_user("test", "test@test.com", "password", invalid_role)
    
    def test_authenticate_user_success(self):
        """測試成功認證邏輯"""
        with patch('app.services.auth_service.User') as mock_user_class:
            # 模擬找到使用者且密碼正確
            mock_user = Mock()
            mock_user.check_password.return_value = True
            mock_user_class.query.filter_by.return_value.first.return_value = mock_user
            
            result = authenticate_user("test@test.com", "correct_password")
            
            # 驗證查詢邏輯
            mock_user_class.query.filter_by.assert_called_once_with(email="test@test.com")
            
            # 驗證密碼檢查
            mock_user.check_password.assert_called_once_with("correct_password")
            
            # 驗證回傳正確使用者
            assert result == mock_user
    
    def test_authenticate_user_wrong_password(self):
        """測試密碼錯誤應回傳 None"""
        with patch('app.services.auth_service.User') as mock_user_class:
            # 模擬找到使用者但密碼錯誤
            mock_user = Mock()
            mock_user.check_password.return_value = False
            mock_user_class.query.filter_by.return_value.first.return_value = mock_user
            
            result = authenticate_user("test@test.com", "wrong_password")
            
            # 驗證回傳 None
            assert result is None
            
            # 驗證密碼檢查被呼叫
            mock_user.check_password.assert_called_once_with("wrong_password")
    
    def test_authenticate_user_not_found(self):
        """測試使用者不存在應回傳 None"""
        with patch('app.services.auth_service.User') as mock_user_class:
            # 模擬找不到使用者
            mock_user_class.query.filter_by.return_value.first.return_value = None
            
            result = authenticate_user("notfound@test.com", "any_password")
            
            # 驗證回傳 None
            assert result is None
            
            # 驗證查詢被執行
            mock_user_class.query.filter_by.assert_called_once_with(email="notfound@test.com")