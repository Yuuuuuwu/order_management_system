# 🛒 OMS 訂單管理系統 - 後端 API

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.1.0-green.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

一個功能完整的訂單管理系統後端 API，基於 Flask 框架開發，提供完整的電子商務後端功能。

## 目前此後端已部署到Render雲端平台上。

網址:https://oms-backend-d0yc.onrender.com

## 📋 目錄

- [功能特色](#-功能特色)
- [技術架構](#-技術架構)


## ✨ 功能特色

### 🔐 認證與授權
- JWT 基礎的身份驗證
- 多角色權限管理（管理員、銷售員、客戶）
- 安全的密碼加密和驗證
- 自動 Token 刷新機制

### 👥 用戶管理
- 完整的用戶 CRUD 操作
- 用戶個人資料管理
- 角色權限分配
- 操作歷史追蹤

### 📦 商品管理
- 多層級商品分類管理
- 商品庫存追蹤
- 促銷價格支援
- 商品圖片管理

### 🛒 訂單管理
- 完整訂單生命週期管理
- 訂單狀態追蹤
- 自動庫存扣減
- 配送資訊管理

### 💳 支付整合
- 綠界科技（ECPay）支付整合
- 多種支付方式支援
- 支付狀態即時同步
- 安全的 MAC 值驗證

### 👤 客戶關係管理
- 客戶資料維護
- 客戶標籤和分類
- 購買歷史分析
- 客戶忠誠度追蹤

### 📊 報表與分析
- 銷售統計報表
- 訂單趨勢分析
- 庫存狀況監控
- 業績儀表板數據

### 🔔 通知系統
- 系統通知管理
- 操作日誌記錄
- 重要事件提醒
- Email 通知整合

## 🏗️ 技術架構

### 核心框架
- **Flask 3.1.0** - 輕量級 Web 框架
- **SQLAlchemy 2.0.40** - ORM 數據庫操作
- **Flask-Migrate** - 數據庫版本控制
- **Flask-JWT-Extended** - JWT 認證管理
- **Flask-CORS** - 跨域請求支援

### 數據庫
- **MySQL 8.0** - 主要關聯式數據庫
- **PostgreSQL** - 生產環境支援（Render 部署）
- **SQLite** - 測試環境

### 開發工具
- **pytest** - 單元測試框架
- **Faker** - 測試數據生成
- **Alembic** - 數據庫遷移工具
- **Gunicorn** - WSGI 服務器

### 部署與容器化
- **Docker** - 容器化部署
- **Docker Compose** - 多容器編排
- **Render** - 雲端部署平台


### 專案結構

```
order_management_system/
├── app/                        # 應用程式主目錄
│   ├── __init__.py            # Flask 應用工廠
│   ├── models/                # 數據模型
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── order.py
│   │   ├── payment.py
│   │   ├── customer.py
│   │   └── notification.py
│   ├── routes/                # API 路由
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── products.py
│   │   ├── orders.py
│   │   ├── payments.py
│   │   └── dashboard.py
│   ├── services/              # 業務邏輯層
│   ├── schemas/               # 數據驗證模式
│   ├── forms/                 # 表單處理
│   └── utils/                 # 工具函數
├── migrations/                # 數據庫遷移檔案
├── scripts/                   # 腳本檔案
├── pytest/                    # 測試檔案
├── config.py                  # 配置檔案
├── run.py                     # 應用程式入口
└── requirements.txt           # Python 依賴
```


感謝所有貢獻者的努力，讓這個專案變得更好！

---

**OMS 訂單管理系統** - 讓電子商務管理變得簡單高效！
