# 使用輕量 Python 映像
FROM python:3.12-slim

# 建立工作目錄
WORKDIR /app

# 設定 Python 環境變數
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    FLASK_ENV=render \
    FLASK_APP=run.py

# 安裝系統依賴
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 複製依賴檔案並安裝 Python 套件
COPY requirements-render.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements-render.txt

# 複製應用程式碼
COPY . .

# 暴露端口
EXPOSE $PORT

# 啟動腳本：顯示環境資訊，執行遷移，載入資料，啟動應用
CMD echo "🔍 Environment Check:" && \
    echo "   FLASK_ENV: $FLASK_ENV" && \
    echo "   DATABASE_URL: ${DATABASE_URL:0:50}..." && \
    echo "🗄️ Running database migrations..." && \
    FLASK_ENV=render flask db upgrade && \
    echo "🌱 Loading seed data..." && \
    FLASK_ENV=render python scripts/seed_data.py; \
    echo "🚀 Starting Gunicorn server..." && \
    gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout 120 run:app
