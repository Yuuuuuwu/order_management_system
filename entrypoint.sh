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

# 2. 啟動 Flask（生產建議 gunicorn）
exec gunicorn --bind 0.0.0.0:5000 "app:create_app()"
