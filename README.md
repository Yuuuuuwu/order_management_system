# 🛒 OMS 訂單管理系統 - 後端 API 

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.1.0-green.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

電子商務訂單管理系統後端 API，基於 Flask，支援多角色權限、商品/訂單/支付/報表/通知等完整功能，並具備完善分層、測試與容器化部署。

### 目前此前端已部署到Render雲端平台，可透過下方測試帳號進行測試。

此為免費方案部署，伺服器會有閒置模式，初次開啟需要等伺服器啟動，若有loading情況請耐心等候，謝謝。

後端網址:https://oms-backend-d0yc.onrender.com

請先開啟後端網址，待後端啟動後顯示Hello, Order Management System，即可開啟下方前端網頁進行測試。

前端網址:https://oms-frontend-ixkl.onrender.com

### 預設測試帳號

```
管理員帳號:
Email: admin@example.com
Password: AdminPassword123!

銷售員帳號:
Email: seller@example.com
Password: SellerPassword123!

客戶帳號:
Email: customer@example.com
Password: CustomerPassword123!
```

---

## 📋 目錄
- [功能特色](#功能特色)
- [API 路由](#api-路由)
- [技術架構](#技術架構)
- [專案結構](#專案結構)
- [測試與部署](#測試與部署)

---

## ✨ 功能特色

### 🔐 認證與授權
- JWT 驗證，支援多角色（admin/seller/customer）
- 密碼雜湊、重設密碼、登入紀錄

### 👥 用戶管理
- 用戶 CRUD、角色分配、個人資料、權限控管

### 📦 商品與分類管理
- 商品 CRUD、上下架、庫存、描述、分類巢狀結構
- 商品多層分類、促銷價、圖片欄位

### 🛒 訂單管理
- 訂單 CRUD、訂單編號、狀態流轉、歷史紀錄
- 訂單明細、庫存自動扣減/恢復、批次狀態更新

### 💳 支付整合
- 綠界 ECPay 金流串接、付款狀態同步、MAC 驗證
- 支援模擬付款、付款紀錄查詢

### 👤 客戶管理
- 客戶 CRUD、標籤、購買歷史、忠誠度

### 📊 報表與儀表板
- 銷售統計、商品排行、客戶分析、月度趨勢
- 儀表板 API、資料分群

### 🔔 通知與日誌
- 系統通知、訂單/付款/狀態異動推播
- 操作日誌、審計追蹤

---

## 🛣️ API 路由（主要）

- `/auth/register`  註冊
- `/auth/login`     登入
- `/auth/me`        取得自己資訊
- `/auth/forgot-password` 忘記密碼
- `/auth/reset-password`  重設密碼
- `/users`          用戶管理
- `/products`       商品管理
- `/categories`     商品分類
- `/orders`         訂單管理
- `/payments`       付款/金流
- `/dashboard/summary` 儀表板統計
- `/notifications`  通知
- `/reports`        報表
- `/customers`      客戶管理
- `/checkout`       結帳流程

---

## 🏗️ 技術架構

- **Flask 3.1.0** / **SQLAlchemy** / **Flask-JWT-Extended**
- **pytest** 單元/整合測試
- **Alembic** 資料庫遷移
- **Docker** / **docker-compose**
- **ECPay** 金流串接

---

## 📁 專案結構

```
order_management_system/
├── app/
│   ├── __init__.py
│   ├── models/         # 數據模型（user, product, order, ...）
│   ├── routes/         # API 路由（auth, users, products, ...）
│   ├── services/       # 業務邏輯（service layer）
│   ├── schemas/        # marshmallow 驗證/序列化
│   ├── forms/          # 表單驗證
│   └── utils/          # 工具（MAC 驗證、email...）
├── migrations/         # Alembic 遷移
├── pytest/             # 測試
├── scripts/            # 初始化/假資料腳本
├── config.py           # 設定
├── run.py              # 入口
├── requirements.txt    # 依賴
├── Dockerfile          # 容器
├── docker-compose.yml  # 多服務協調
└── README.md
```

---

## 🧪 測試與部署
- `pytest/` 單元/整合測試
- `docker-compose up` 一鍵啟動
- 支援本地/雲端部署

