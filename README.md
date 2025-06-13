# Order Management System (OMS)

## 專案結構

```
app/
  models/      # 資料庫 ORM Model (user, product, order, payment...)
  schemas/     # Marshmallow Schema 驗證/序列化
  services/    # 商業邏輯/資料存取 (Service Layer)
  utils/       # 工具函式 (email, jwt, password...)
  forms/       # 表單驗證 (Marshmallow Form)
  routes/      # API 路由 (Blueprint)
```

## 主要功能
- 使用者註冊、登入、密碼找回
- 商品管理 CRUD
- 訂單管理、訂單明細
- 付款資訊管理
- 權限控管（admin/user）

## 啟動方式
1. 安裝依賴：`pip install -r requirements.txt`
2. 啟動 MySQL（建議用 docker-compose）
3. 初始化資料庫：`flask db upgrade`
4. 啟動伺服器：`flask run`

## API 文件
- Swagger UI: http://localhost:5000/apidocs/

## 密碼找回流程
1. POST `/auth/forgot-password` 輸入 email，取得重設 token（測試用直接回傳）。
2. POST `/auth/reset-password` 輸入 token、新密碼，完成重設。

## 目錄說明
- `models/`：每個資料表一個 model 檔案，單一職責。
- `schemas/`：每個資源一個 schema，欄位驗證與序列化。
- `services/`：封裝商業邏輯，controller/route 呼叫。
- `utils/`：工具類，密碼雜湊、jwt、寄信等。
- `forms/`：表單驗證，與前端欄位對應。
- `routes/`：API 路由，分資源模組化。

## 綠界支付（ECPay）模擬
- `/payments/ecpay/<order_id>`：產生綠界付款連結與參數（POST，需 JWT）
- `/payments/ecpay/callback`：綠界付款通知（ECPay 伺服器呼叫，會自動更新訂單狀態）
- 請參考 [ECPay 官方文件](https://developers.ecpay.com.tw/?p=2856)

## 最佳化與部署
- 已支援 Docker、環境變數、CORS、JWT、資料庫自動 migrate
- 請於 `.env` 設定金鑰與 ECPay 測試參數

---

如需更多說明，請參考原始碼註解。
