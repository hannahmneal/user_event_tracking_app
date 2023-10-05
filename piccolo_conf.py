import os
from dotenv import load_dotenv
from piccolo.conf.apps import AppRegistry
from piccolo.engine.postgres import PostgresEngine

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_PORT = os.getenv("DB_PORT")

DB = PostgresEngine(config={
    'database': DB_NAME,
    'host': DB_HOST,
    'password': DB_PASS,
    'port': DB_PORT,
    'user': DB_USER,
})

APP_REGISTRY = AppRegistry(apps=['api.db.piccolo_app'])
