from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

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

# Function to get a database session
def get_db():
    db: Session = SessionLocal()
    try:
        yield db  # Fournit la session à la route
    finally:
        db.close()  # Ferme la session après usage

Base = declarative_base()