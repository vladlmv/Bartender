from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from myapp import Base

DATABASE_URL = "postgresql://postgres:1928@localhost/postgres"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)