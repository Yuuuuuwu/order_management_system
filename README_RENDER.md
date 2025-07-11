# 🐳 Render Docker 部署 - 純淨版

## ⚠️ 解決 "build.sh not found" 錯誤

### 問題：
Render 控制台可能還有舊的 Build Command 設定在尋找 `build.sh`

### 解決方法：

#### 1. 清理 Render 設定
在你的 Render Web Service 設定頁面：

**Build Command**: 留空或刪除內容
**Start Command**: 留空或刪除內容  
**Docker Command**: 留空或刪除內容

#### 2. 確認環境設定
- **Environment**: 選擇 `Docker` (不是 Python)
- **Dockerfile Path**: 留空 (使用根目錄的 Dockerfile)

#### 3. 環境變數
```
FLASK_ENV=render
FLASK_APP=run.py
DATABASE_URL=<你的 PostgreSQL 連接字串>
JWT_SECRET_KEY=your-secret-key
SECRET_KEY=your-flask-secret-key
FRONTEND_URL=your-frontend-url
```

#### 4. 重新部署
清理設定後點擊 "Manual Deploy" → "Deploy Latest Commit"

## 📋 檔案檢查清單

確認以下檔案存在且正確：

- ✅ `Dockerfile` - Docker 建置檔案
- ✅ `requirements-render.txt` - Python 依賴
- ✅ `run.py` - Flask 應用入口
- ✅ `scripts/seed_data.py` - 初始資料腳本
- ❌ **不需要任何 .sh 檔案**
- ❌ **不需要 render.yaml**

## 🎯 預期行為

Docker 容器會自動：
1. 安裝 Python 依賴
2. 執行資料庫遷移
3. 載入初始資料  
4. 啟動 Gunicorn 服務器

## 🔍 除錯

如果還是失敗，檢查：
1. Render 服務是否選擇了 "Docker" 環境
2. Build/Start Command 是否已清空
3. 環境變數是否正確設定
4. PostgreSQL 資料庫是否已建立並連接