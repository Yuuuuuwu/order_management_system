# 🐳 Render Docker 部署指南

## 最簡單的部署方式

### 1. 建立 PostgreSQL 資料庫
1. 登入 [Render](https://render.com)
2. 點擊 "New" → "PostgreSQL"
3. 設定：
   - Name: `oms-database`
   - Database Name: `oms_db`
   - User: `oms_user`
   - Plan: Free

### 2. 建立 Web Service
1. 點擊 "New" → "Web Service"
2. 連接你的 Git 儲存庫
3. 設定：
   - **Name**: `oms-backend`
   - **Environment**: `Docker`
   - **Plans**: Free

### 3. 環境變數設定
在 Web Service 的 Environment Variables 中加入：

```
FLASK_ENV=render
FLASK_APP=run.py
DATABASE_URL=<PostgreSQL 連接字串>
JWT_SECRET_KEY=your-secret-key-here
SECRET_KEY=your-flask-secret-key-here
FRONTEND_URL=https://your-frontend-url.com
```

**重要**: `DATABASE_URL` 可以在 PostgreSQL 資料庫頁面的 "Connections" 中找到

### 4. 部署
- 點擊 "Deploy Latest Commit"
- Render 會自動：
  1. 建置 Docker 映像
  2. 執行資料庫遷移
  3. 載入初始資料
  4. 啟動 Gunicorn 服務器

## 預設測試帳號
部署完成後可使用：
- 管理員: `admin@example.com` / `AdminPassword123!`
- 銷售員: `seller@example.com` / `SellerPassword123!`
- 客戶: `customer@example.com` / `CustomerPassword123!`

## 故障排除
1. **部署失敗**: 檢查 Deploy Logs
2. **資料庫連接失敗**: 確認 DATABASE_URL 正確
3. **應用無法啟動**: 檢查環境變數設定

就是這麼簡單！不需要任何 .sh 腳本或 YAML 檔案。