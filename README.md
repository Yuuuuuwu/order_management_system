# 訂單管理系統 (Order Management System)

## 專案簡介

這是一個基於 Flask 的訂單管理系統，提供完整的電子商務後端功能，包括用戶管理、商品管理、訂單處理、支付整合和客戶關係管理。系統設計為支援多種角色（管理員、銷售員、客戶），並整合綠界科技支付平台。

## 主要功能

### 🔐 用戶認證與授權
- 用戶註冊與登入
- JWT 令牌驗證
- 多角色權限管理（admin、seller、customer）
- 密碼安全加密

### 👥 用戶管理
- 用戶資料維護
- 角色權限設定
- 帳號狀態管理
- 登入歷史追蹤

### 📦 商品管理
- 商品分類管理（支援多層級）
- 商品資料維護
- 庫存管理
- 促銷價格設定

### 🛒 訂單管理
- 訂單建立與追蹤
- 訂單狀態管理
- 訂單項目詳情
- 訂單歷史記錄
- 配送資訊管理

### 💳 支付整合
- 綠界科技支付平台整合
- 多種支付方式支援
- 支付狀態追蹤
- 交易記錄管理

### 👤 客戶管理
- 客戶資料管理
- 客戶標籤系統
- 客戶訂單記錄

### 📊 報表與儀表板
- 銷售統計報表
- 訂單趨勢分析
- 庫存狀況監控
- 業績儀表板

### 🔔 通知系統
- 系統通知管理
- 操作日誌記錄
- 重要事件提醒

## 技術架構

### 後端框架
- **Flask** - 輕量級 Web 框架
- **Flask-SQLAlchemy** - ORM 數據庫操作
- **Flask-Migrate** - 數據庫遷移管理
- **Flask-JWT-Extended** - JWT 認證
- **Flask-CORS** - 跨域請求支援

### 數據庫
- **MySQL 8.0** - 主要數據庫
- **SQLAlchemy** - ORM 映射
- **Alembic** - 數據庫版本控制

### 部署與容器化
- **Docker** - 容器化部署
- **Docker Compose** - 多容器編排
- **Gunicorn** - WSGI 服務器

### 開發工具
- **pytest** - 單元測試
- **Faker** - 測試數據生成
- **python-dotenv** - 環境變數管理

## 專案結構

```
order_management_system/
├── app/                          # 應用程式主目錄
│   ├── __init__.py              # Flask 應用程式工廠
│   ├── models/                  # 數據模型
│   │   ├── user.py             # 用戶模型
│   │   ├── product.py          # 商品模型
│   │   ├── order.py            # 訂單模型
│   │   ├── payment.py          # 支付模型
│   │   └── customer.py         # 客戶模型
│   ├── routes/                  # 路由處理
│   │   ├── auth.py             # 認證路由
│   │   ├── users.py            # 用戶管理
│   │   ├── products.py         # 商品管理
│   │   ├── orders.py           # 訂單管理
│   │   ├── payments.py         # 支付處理
│   │   └── dashboard.py        # 儀表板
│   ├── services/                # 業務邏輯服務
│   ├── schemas/                 # 數據驗證模式
│   ├── forms/                   # 表單處理
│   └── utils/                   # 工具函數
├── migrations/                   # 數據庫遷移檔案
├── scripts/                     # 腳本檔案
│   └── seed_data.py            # 初始數據填充
├── pytest/                      # 測試檔案
├── config.py                    # 配置檔案
├── run.py                       # 應用程式入口
├── requirements.txt             # Python 依賴
├── Dockerfile                   # Docker 映像配置
├── docker-compose.yml           # Docker 編排配置
└── entrypoint.sh               # 容器啟動腳本
```

## 安裝與部署

### 環境需求
- Python 3.8+
- Docker & Docker Compose
- MySQL 8.0

### 使用 Docker 快速部署

1. **複製專案**
   ```bash
   git clone <repository-url>
   cd order_management_system
   ```

2. **設定環境變數**
   ```bash
   cp .env.example .env
   # 編輯 .env 檔案，設定必要的環境變數
   ```

3. **啟動服務**
   ```bash
   docker-compose up -d
   ```

4. **初始化數據庫**
   ```bash
   # 數據庫遷移和初始數據會自動執行
   # 可透過以下指令手動執行
   docker-compose exec app flask db upgrade
   docker-compose exec app python scripts/seed_data.py
   ```

### 本地開發環境

1. **安裝依賴**
   ```bash
   pip install -r requirements.txt
   ```

2. **設定環境變數**
   ```bash
   export FLASK_APP=run.py
   export FLASK_ENV=development
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

## 環境變數配置

在 `.env` 檔案中設定以下變數：

```env
# 數據庫配置
DATABASE_URL=mysql+pymysql://jenny:1234@db:3306/my_db

# JWT 密鑰
JWT_SECRET_KEY=your-secret-key
SECRET_KEY=your-flask-secret-key

# 綠界支付配置
ECPAY_MERCHANT_ID=your-merchant-id
ECPAY_HASH_KEY=your-hash-key
ECPAY_HASH_IV=your-hash-iv
ECPAY_NOTIFY_URL=http://your-domain/payment/notify
ECPAY_ORDER_RETURN_URL=http://your-domain/payment/return

# 前後端 URL
FRONTEND_URL=http://localhost:5173
BACKEND_URL=http://localhost:5000
```

## API 文件

系統提供 RESTful API，主要端點包括：

### 認證相關
- `POST /auth/register` - 用戶註冊
- `POST /auth/login` - 用戶登入
- `POST /auth/logout` - 用戶登出

### 用戶管理
- `GET /users` - 獲取用戶列表
- `GET /users/{id}` - 獲取用戶詳情
- `PUT /users/{id}` - 更新用戶資料
- `DELETE /users/{id}` - 刪除用戶

### 商品管理
- `GET /products` - 獲取商品列表
- `POST /products` - 新增商品
- `PUT /products/{id}` - 更新商品
- `DELETE /products/{id}` - 刪除商品

### 訂單管理
- `GET /orders` - 獲取訂單列表
- `POST /orders` - 建立新訂單
- `GET /orders/{id}` - 獲取訂單詳情
- `PUT /orders/{id}` - 更新訂單狀態

### 支付處理
- `POST /payments/create` - 建立支付
- `POST /payments/notify` - 支付回調通知
- `GET /payments/{id}` - 獲取支付狀態

## 測試

執行單元測試：

```bash
# 使用 pytest 執行測試
pytest

# 執行特定測試檔案
pytest pytest/test_users.py

# 顯示測試覆蓋率
pytest --cov=app
```

## 資料庫管理

### 創建新的遷移
```bash
flask db migrate -m "描述變更內容"
```

### 應用遷移
```bash
flask db upgrade
```

### 降級遷移
```bash
flask db downgrade
```

## 生產環境部署

1. **設定生產環境變數**
   ```bash
   export FLASK_ENV=production
   ```

2. **使用 Gunicorn 啟動**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 run:app
   ```

3. **配置反向代理**
   建議使用 Nginx 作為反向代理服務器

## 常見問題

### Q: 如何重置數據庫？
A: 停止容器，刪除數據卷，重新啟動：
```bash
docker-compose down -v
docker-compose up -d
```

### Q: 如何查看應用程式日誌？
A: 使用 Docker Compose 查看日誌：
```bash
docker-compose logs -f app
```

### Q: 如何新增新的 API 端點？
A: 在 `app/routes/` 目錄下新增路由檔案，並在 `app/__init__.py` 中註冊 Blueprint。

## 貢獻指南

1. Fork 此專案
2. 建立功能分支 (`git checkout -b feature/new-feature`)
3. 提交變更 (`git commit -am 'Add new feature'`)
4. 推送分支 (`git push origin feature/new-feature`)
5. 建立 Pull Request

## 授權

此專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 檔案

## 聯絡資訊

如有問題或建議，請聯絡：
- 開發者：[Your Name]
- Email：[your.email@example.com]
- 專案 Issues：[Repository Issues URL]

---
*最後更新：2024年6月*