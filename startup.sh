#! /bin/sh

echo "⏳ Setting up database..."
# start db
docker compose up -d db

sleep 2

echo "📦 Loading requirements... "
# load requirements
pip install --no-cache-dir -r requirements.txt

sleep 2

echo "✅ Starting api..."
# start api
uvicorn api.server:app --port 8080 --reload --log-level info