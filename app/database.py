import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from sqlalchemy import text
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


print("DATABASE_URL =", DATABASE_URL)

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set")

engine = create_engine(DATABASE_URL, pool_pre_ping=True,connect_args={"options": "-csearch_path=public"})



with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM public.products"))
    print(result.scalar())
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()
