#!/bin/bash
# 測試執行腳本

echo "🧪 開始執行測試..."

# 設定環境變數
export FLASK_ENV=testing
export FLASK_APP=run.py

# 執行測試
echo "📋 執行單元測試..."
pytest pytest/test_users.py pytest/test_validation.py pytest/test_auth.py -v

echo "🛍️ 執行商品測試..."
pytest pytest/test_products.py -v

echo "📦 執行訂單測試..."
pytest pytest/test_orders.py -v

echo "💳 執行付款測試..."
pytest pytest/test_payments.py -v

echo "🔗 執行整合測試..."
pytest pytest/test_integration.py -v

echo "📊 執行完整測試並產生覆蓋率報告..."
pytest --cov=app --cov-report=html --cov-report=term

echo "✅ 測試完成！"
echo "📊 覆蓋率報告已產生至 htmlcov/ 目錄"