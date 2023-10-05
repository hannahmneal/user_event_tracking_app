MAKEFLAGS += --no-builtin-rules

###################################################
# API AND STARTUP
###################################################

api-start-local:
	@setup-db
	echo "⏳ Setting up database..." && sleep 3
	@start-api
	echo "✅ Starting api..."

setup-db:
	@docker compose up -d db

start-api:
	@uvicorn api.server:app --port 8080 --reload --log-level info

###################################################
# DB AND MIGRATIONS
###################################################
