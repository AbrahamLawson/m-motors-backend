from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://fastapi_user:fastapi_pass@127.0.0.1:3306/fastapi_db"

# Init the connection with dataBase
try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_recycle=3600)
    print("Database connection successful!")
except Exception as e:
    print(f"Error connecting to database: {e}")
    raise e

# Create session 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()