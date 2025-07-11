#!/usr/bin/env sh
set -e

# 從 DATABASE_URL (例如 postgresql://user:pass@host:5432/dbname) 解析 host 與 port
DB_HOST="$(echo "$DATABASE_URL" | sed -E 's#.*@([^:/]+):?[0-9]*/.*#\1#')"
DB_PORT="$(echo "$DATABASE_URL" | sed -E 's#.*:([0-9]+)/.*#\1#')"
# 若沒抓到 port，預設 5432
DB_PORT="${DB_PORT:-5432}"

echo "⏳ Waiting for database at $DB_HOST:$DB_PORT ..."
while ! nc -z "$DB_HOST" "$DB_PORT"; do
  echo "   still waiting for $DB_HOST:$DB_PORT ..."
  sleep 1
done
echo "✅ Database is up!"

# 執行資料庫遷移（需要安裝 flask-migrate）
echo "🚀 Running migrations..."
flask db upgrade

# 如有需要，可以在此呼叫 seed_data
# echo "🌱 Seeding initial data..."
# python scripts/seed_data.py

# 最後交給 CMD 啟動 app
exec "$@"
