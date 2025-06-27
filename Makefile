.PHONY: init migrate up logs

# 1. 從零初始化 migrations + local DB
init:
	docker compose down -v
	docker compose up -d db
	@echo "等待 DB 啟動…"; \
	until docker compose exec db mysqladmin ping -h "db" --silent; do sleep 1; done
	docker compose exec app flask db init
	docker compose exec app flask db migrate -m "initial schema"
	docker compose exec app flask db upgrade

# 2. 當 model 有改動時
migrate:
	@read -p "Migration message: " msg; \
	docker compose exec app flask db migrate -m "$$msg"; \
	docker compose exec app flask db upgrade; \
	git add migrations/; git commit -m "chore: $$msg"

# 3. 啟動／重建容器
up:
	docker compose down -v
	docker compose up -d --build

# 4. 觀察日誌
logs:
	docker compose logs -f app

# 使用方式
# 第一次初始化
#   make init
# 修改 model 後
#   make migrate
# 啟動／重建服務
#   make up
# 看日誌確認
#   make logs
