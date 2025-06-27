# 1. 選擇基底映像
FROM python:3.12-slim

# 2. 設定工作目錄
WORKDIR /app


# 2.1 設定環境變數
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

# 2.2 安裝系統相依套件
RUN apt-get update && apt-get install -y \
      build-essential \
      python3-dev \
      netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# 3. 安裝 Python 套件：先升級 pip，再安裝 requirements 裡的所有相依套件
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# 4. 複製程式碼
COPY . .

# 5. 設定環境變數（告訴 Flask 啟動哪個 app）
ENV FLASK_APP=run.py \
    FLASK_ENV=production \
    DATABASE_URL="mysql+pymysql://jenny:1234@db:3306/my_db"

# 6. 暴露對外的 port
EXPOSE 5000

# 7. 啟動指令
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
