import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import text

with engine.connect() as conn:
    db_name = conn.execute(text("SELECT current_database()")).scalar()
    schema = conn.execute(text("SELECT current_schema()")).scalar()
    print("CONNECTED DATABASE =", db_name)
    print("CURRENT SCHEMA =", schema)
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args={"options": "-csearch_path=public"},
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()
