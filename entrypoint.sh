#!/bin/sh
set -e

# 1. 自動套用所有還沒跑過的 migration
flask db upgrade

# 2. 啟動 Flask（生產建議 gunicorn）
exec gunicorn -b 0.0.0.0:5000 run:app
