#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
資料庫初始化腳本

根據環境變數決定是否載入 seed data：
- LOAD_SEED_DATA=true: 載入測試資料
- LOAD_SEED_DATA=false 或未設定: 只執行 migration，不載入測試資料

使用方式：
    python scripts/init_db.py
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from flask_migrate import upgrade

def init_database():
    """初始化資料庫"""
    app = create_app()
    
    with app.app_context():
        # 執行 migration
        print("正在執行資料庫 migration...")
        upgrade()
        print("Migration 完成")
        
        # 檢查是否需要載入 seed data
        load_seed = os.getenv('LOAD_SEED_DATA', 'false').lower() == 'true'
        
        if load_seed:
            print("正在載入 seed data...")
            # 導入並執行 seed data
            from scripts.seed_data import main as load_seed_data
            load_seed_data()
            print("Seed data 載入完成")
        else:
            print("跳過 seed data 載入（LOAD_SEED_DATA != true）")

if __name__ == '__main__':
    init_database()