#!/usr/bin/env python3
"""
測試 Render 配置腳本
用於驗證環境變數和配置是否正確
"""
import os
import sys

# 確保環境變數設定
os.environ['FLASK_ENV'] = 'render'
os.environ['FLASK_APP'] = 'run.py'

try:
    from app import create_app
    
    print("🔍 Testing Render Configuration...")
    print(f"   FLASK_ENV: {os.getenv('FLASK_ENV')}")
    print(f"   DATABASE_URL: {os.getenv('DATABASE_URL', 'NOT SET')[:50]}...")
    
    app = create_app()
    
    print(f"✅ Flask app created successfully!")
    print(f"   Config class: {app.config.__class__.__name__}")
    print(f"   Database URI: {app.config.get('SQLALCHEMY_DATABASE_URI', 'NOT SET')[:50]}...")
    print(f"   Debug mode: {app.config.get('DEBUG', 'NOT SET')}")
    
    # 測試資料庫連接
    with app.app_context():
        from app import db
        try:
            # 嘗試連接資料庫
            db.engine.execute("SELECT 1")
            print("✅ Database connection successful!")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
    
except Exception as e:
    print(f"❌ Configuration test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)