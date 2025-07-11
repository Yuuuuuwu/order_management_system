#!/bin/sh
set -e

echo "⏳ Waiting for database to be ready…"
# 下面這行會每秒檢查 db:3306 port，直到成功
until nc -z db 3306; do
  sleep 1
done

echo "✅ Database is up, running migrations"
# 1. 自動套用所有還沒跑過的 migration
flask db upgrade

echo "🌱 Loading seed data..."
# 2. 載入預設資料
python scripts/seed_data.py

echo "🚀 Starting Flask application"
# 3. 啟動 Flask（生產建議 gunicorn）
exec gunicorn --bind 0.0.0.0:5000 "app:create_app()"
