# 🚀 Render 部署指南

## 部署步驟

### 1. 準備工作
1. 將所有變更提交到 Git 儲存庫
2. 確保 `render.yaml` 檔案在專案根目錄

### 2. Render 部署
1. 登入 [Render](https://render.com)
2. 點擊 "New" → "Blueprint"
3. 連接你的 Git 儲存庫
4. Render 會自動讀取 `render.yaml` 配置並創建服務

### 3. 服務包含
- **Web 服務**: Flask 後端 API
- **PostgreSQL 資料庫**: 自動創建並連接

### 4. 自動執行
- ✅ 安裝 Python 依賴
- ✅ 資料庫遷移
- ✅ 載入初始資料
- ✅ 啟動 Gunicorn 服務器

### 5. 預設測試帳號
部署完成後可使用以下帳號測試：
- 管理員: `admin@example.com` / `AdminPassword123!`
- 銷售員: `seller@example.com` / `SellerPassword123!`
- 客戶: `customer@example.com` / `CustomerPassword123!`

### 6. 注意事項
- 記得在 `render.yaml` 中更新你的 Git 儲存庫 URL
- 如需修改環境變數，直接編輯 `render.yaml`
- 部署過程會自動執行，無需手動設定

## 故障排除

如果部署失敗，檢查：
1. Git 儲存庫 URL 是否正確
2. `requirements-render.txt` 是否存在
3. 檢查 Render 部署日誌中的錯誤訊息