from sqlalchemy.orm import sessionmaker, base
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

# database connection string
DB_URL = 'postgresql+psycopg2://postgres:postgres@localhost/payments'

# engine object and sessionmaker

engine = create_engine(DB_URL)
sessionmaker = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

def get_db():
    db = sessionmaker()
    try:
        yield db
    finally:
        db.close()