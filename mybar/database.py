from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from mybar.myapp import Base

DATABASE_URL = "postgresql://postgres:1928@localhost/postgres"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

import psycopg2

def init_db():
    Base.metadata.create_all(bind=engine)
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="1928",
            host="localhost"
        )
        return conn
    except Exception as e:
        print(f"Connection error: {e}")
        return None