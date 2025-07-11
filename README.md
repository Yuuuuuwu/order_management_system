# 🛒 OMS 訂單管理系統 - 後端 API

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.1.0-green.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

一個功能完整的訂單管理系統後端 API，基於 Flask 框架開發，提供完整的電子商務後端功能。

## 📋 目錄

- [功能特色](#-功能特色)
- [技術架構](#-技術架構)
- [快速開始](#-快速開始)
- [API 文檔](#-api-文檔)
- [開發指南](#-開發指南)
- [部署](#-部署)
- [測試](#-測試)
- [貢獻指南](#-貢獻指南)

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

## 🚀 快速開始

### 前置需求
- Python 3.8 或更高版本
- Docker 和 Docker Compose（推薦）
- MySQL 8.0（本地開發）

### 使用 Docker（推薦）

1. **克隆專案**
   ```bash
   git clone <repository-url>
   cd order_management_system
   ```

2. **初始化並啟動服務**
   ```bash
   # 完整初始化（首次運行）
   make init
   
   # 或使用 Docker Compose
   docker-compose up -d --build
   ```

3. **檢查服務狀態**
   ```bash
   docker-compose ps
   docker-compose logs -f app
   ```

### 本地開發

1. **安裝依賴**
   ```bash
   pip install -r requirements.txt
   ```

2. **設定環境變數**
   ```bash
   export FLASK_APP=run.py
   export FLASK_ENV=development
   export DATABASE_URL="mysql+pymysql://user:password@localhost:3306/oms_db"
   ```

3. **初始化數據庫**
   ```bash
   flask db upgrade
   python scripts/seed_data.py
   ```

4. **啟動開發服務器**
   ```bash
   python run.py
   ```

服務將在 `http://localhost:5000` 上運行。

## 🔧 環境配置

### 必要環境變數

```bash
# Flask 基本配置
FLASK_APP=run.py
FLASK_ENV=development  # development, production, render

# 數據庫配置
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/oms_db

# 安全密鑰
JWT_SECRET_KEY=your-super-secure-jwt-secret-key
SECRET_KEY=your-flask-secret-key

# 前後端 URL
FRONTEND_URL=http://localhost:5173
BACKEND_URL=http://localhost:5000

# ECPay 支付配置（可選）
ECPAY_MERCHANT_ID=your-merchant-id
ECPAY_HASH_KEY=your-hash-key
ECPAY_HASH_IV=your-hash-iv
ECPAY_NOTIFY_URL=http://your-domain/payments/notify
ECPAY_ORDER_RETURN_URL=http://your-domain/payments/return
```

### 配置檔案

專案支援多種環境配置：

- `DevelopmentConfig` - 本地開發環境
- `TestingConfig` - 測試環境
- `ProductionConfig` - 生產環境
- `RenderConfig` - Render 平台部署

## 📚 API 文檔

### 認證相關
```http
POST /auth/register    # 用戶註冊
POST /auth/login       # 用戶登入
POST /auth/logout      # 用戶登出
POST /auth/refresh     # 刷新 Token
```

### 用戶管理
```http
GET    /users          # 獲取用戶列表
GET    /users/{id}     # 獲取用戶詳情
POST   /users          # 創建用戶
PUT    /users/{id}     # 更新用戶
DELETE /users/{id}     # 刪除用戶
```

### 商品管理
```http
GET    /products       # 獲取商品列表
GET    /products/{id}  # 獲取商品詳情
POST   /products       # 創建商品
PUT    /products/{id}  # 更新商品
DELETE /products/{id}  # 刪除商品

GET    /categories     # 獲取分類列表
POST   /categories     # 創建分類
```

### 訂單管理
```http
GET    /orders         # 獲取訂單列表
GET    /orders/{id}    # 獲取訂單詳情
POST   /orders         # 創建訂單
PUT    /orders/{id}    # 更新訂單狀態
DELETE /orders/{id}    # 取消訂單
```

### 支付處理
```http
POST   /payments/create   # 創建支付
POST   /payments/notify   # 支付回調通知
GET    /payments/{id}     # 獲取支付狀態
```

### 儀表板
```http
GET    /dashboard/stats   # 獲取統計數據
GET    /reports/sales     # 銷售報表
GET    /reports/orders    # 訂單報表
```

## 🛠️ 開發指南

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

### 數據庫遷移

```bash
# 創建新遷移
flask db migrate -m "描述變更內容"

# 應用遷移
flask db upgrade

# 降級遷移
flask db downgrade

# 查看遷移歷史
flask db history
```

### 添加新功能

1. **創建數據模型**：在 `app/models/` 中定義新的模型
2. **創建遷移**：使用 `flask db migrate` 生成遷移文件
3. **添加業務邏輯**：在 `app/services/` 中實現業務邏輯
4. **創建 API 路由**：在 `app/routes/` 中定義 API 端點
5. **添加驗證模式**：在 `app/schemas/` 中定義數據驗證
6. **編寫測試**：在 `pytest/` 中添加單元測試

## 🧪 測試

### 運行測試

```bash
# 運行所有測試
pytest

# 運行特定測試檔案
pytest pytest/test_users.py

# 運行測試並顯示覆蓋率
pytest --cov=app

# 運行測試並生成 HTML 覆蓋率報告
pytest --cov=app --cov-report=html
```

### 測試數據

使用 `scripts/seed_data.py` 生成測試數據：

```bash
python scripts/seed_data.py
```

預設測試帳號：
- 管理員：`admin@example.com` / `AdminPassword123!`
- 銷售員：`seller@example.com` / `SellerPassword123!`
- 客戶：`customer@example.com` / `CustomerPassword123!`

## 🚀 部署

### Docker 部署

```bash
# 構建並啟動所有服務
docker-compose up -d --build

# 查看服務狀態
docker-compose ps

# 查看日誌
docker-compose logs -f app
```

### Render 部署

1. **配置檔案**：使用 `requirements-render.txt` 和 `RenderConfig`
2. **建置腳本**：`build.sh` 處理依賴安裝和數據庫遷移
3. **啟動腳本**：`start.sh` 使用 Gunicorn 啟動服務
4. **環境變數**：設定必要的環境變數

詳細部署指南請參考 `RENDER_部署教學.md`。

### 生產環境注意事項

- 使用強密碼設定所有密鑰
- 啟用 HTTPS
- 配置反向代理（Nginx）
- 設定資料庫備份
- 監控服務健康狀態
- 設定日誌輪轉

## 🤝 貢獻指南

1. **Fork 專案**
2. **創建功能分支** (`git checkout -b feature/amazing-feature`)
3. **提交變更** (`git commit -m 'Add some amazing feature'`)
4. **推送分支** (`git push origin feature/amazing-feature`)
5. **開啟 Pull Request**

### 代碼規範

- 遵循 PEP 8 Python 代碼風格
- 為新功能添加單元測試
- 更新相關文檔
- 確保所有測試通過

## 📄 授權

本專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 檔案。

## 📞 支援

- **問題回報**：[GitHub Issues](https://github.com/your-repo/issues)
- **功能請求**：[GitHub Discussions](https://github.com/your-repo/discussions)
- **文檔**：專案 Wiki 頁面

## 🙏 致謝

感謝所有貢獻者的努力，讓這個專案變得更好！

---

**OMS 訂單管理系統** - 讓電子商務管理變得簡單高效！