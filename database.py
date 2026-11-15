import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Load database URL strictly from environment variables
raw_url = os.getenv("DATABASE_URL") or os.getenv("Database_URL")

if not raw_url:
    raise ValueError(
        "DATABASE_URL environment variable is not set. "
        "Please configure your PostgreSQL connection string in the .env file. "
        "Refer to .env.example for details."
    )

# Normalize postgres:// or postgresql:// to postgresql+psycopg2:// for SQLAlchemy compatibility
if raw_url.startswith("postgres://"):
    raw_url = raw_url.replace("postgres://", "postgresql+psycopg2://", 1)
elif raw_url.startswith("postgresql://") and not raw_url.startswith("postgresql+psycopg2://"):
    raw_url = raw_url.replace("postgresql://", "postgresql+psycopg2://", 1)

DATABASE_URL = raw_url

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Dependency that yields a SQLAlchemy database session
    and ensures proper cleanup after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
