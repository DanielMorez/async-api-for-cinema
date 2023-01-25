import redis
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import MetaData, event
from sqlalchemy.schema import DDL

from config import settings

metadata_obj = MetaData(schema=settings.pg_schema)

db = SQLAlchemy(metadata=metadata_obj)
cache_storage = redis.Redis(
    host=settings.redis_dsn.host,
    port=settings.redis_dsn.port,
    decode_responses=True,
)


def init_db(app: Flask):
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.pg_dsn
    db.init_app(app)
    event.listen(
        db.metadata,
        "before_create",
        DDL(f"CREATE SCHEMA IF NOT EXISTS {settings.pg_schema}"),
    )


def init_migrate(app: Flask, database: SQLAlchemy):
    Migrate(app, database)
