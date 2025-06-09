.PHONY: init migrate up logs

# 1. 從零初始化 migrations + local DB
init:
	rm -rf migrations
	mysql -ujenny -p1234 -h localhost -P3307 -e "DROP DATABASE IF EXISTS my_db; CREATE DATABASE my_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
	export FLASK_APP=run.py DATABASE_URL="mysql+pymysql://jenny:1234@localhost:3307/my_db" && \
	flask db init && \
	flask db migrate -m "initial schema" && \
	flask db upgrade

# 2. 當 model 有改動時
migrate:
	@read -p "Migration message: " msg; \
	export FLASK_APP=run.py DATABASE_URL="mysql+pymysql://jenny:1234@localhost:3307/my_db" && \
	flask db migrate -m "$$msg" && \
	flask db upgrade && \
	git add migrations/ && git commit -m "chore: $$msg"

# 3. 啟動容器
up:
	docker-compose down -v
	docker-compose up -d --build

# 4. 觀察日誌
logs:
	docker-compose logs -f app

# 使用方式
# 第一次初始化
# make init

# 修改 model 後
# make migrate

# 啟動／重建容器
# make up

# 看日誌確認
# make logs
