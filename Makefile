MAKEFLAGS += --no-builtin-rules

###################################################
# API AND STARTUP
###################################################

api-start-local:
	echo "⏳ Setting up database..."
	@make setup-db
	sleep 2
	echo "📦 Loading requirements... "
	@make load-requirements
	sleep 2
	echo "✅ Starting api..."
	@make start-api

load-requirements:
	@pip install --no-cache-dir -r requirements.txt
	
setup-db:
	@docker compose up -d db

start-api:
	@uvicorn api.server:app --port 8080 --reload --log-level info


###################################################
# DB AND MIGRATIONS
###################################################
