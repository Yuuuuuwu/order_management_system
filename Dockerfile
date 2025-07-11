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

# 啟動腳本：先執行遷移，再啟動應用
CMD flask db upgrade && \
    python scripts/seed_data.py; \
    gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout 120 run:app
