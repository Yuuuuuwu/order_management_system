# 1. 使用輕量映像
FROM python:3.12-slim

# 2. 建立工作目錄
WORKDIR /app

# 3. 設定 Python 環境
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# 4. 安裝系統相依套件（含 netcat）
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential python3-dev netcat-openbsd \
 && rm -rf /var/lib/apt/lists/*

# 5. 安裝 Python 套件
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# 6. 複製程式碼與等待腳本
COPY . .
COPY wait-for-db.sh /wait-for-db.sh
RUN chmod +x /wait-for-db.sh

# 7. 暴露 Port
EXPOSE 5000

# 8. 啟動前先等資料庫，再啟動 Gunicorn
ENTRYPOINT ["/wait-for-db.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "run:app"]
