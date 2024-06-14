from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv


load_dotenv()

# environment variables
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')

# Database URL for SQLAlchemy
SQLALCHEMY_DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

# database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()
