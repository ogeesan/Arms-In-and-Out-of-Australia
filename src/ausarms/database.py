"""Database connection and session management."""

import os
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from typing import Optional

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_database_path() -> str:
    """Get the database file path."""
    return 'ausarms.db'

def get_database_url(db_type: str = "sqlite") -> str:
    """Get database URL based on environment or type."""
    database_path = get_database_path()
    if db_type == "sqlite":
        return f"sqlite:///{database_path}"
    elif db_type == "postgresql":
        raise NotImplementedError("PostgreSQL configuration not implemented.")
        # You can also use environment variables here
        user = os.getenv("DB_USER", "username")
        password = os.getenv("DB_PASSWORD", "password")
        host = os.getenv("DB_HOST", "localhost")
        return f"postgresql://{user}:{password}@{host}/{database_path}"
    else:
        raise ValueError(f"Unsupported database type: {db_type}")


def create_engine(db_type: str = "sqlite") -> sa.Engine:
    """Create SQLAlchemy engine."""
    url = get_database_url(db_type)
    engine = sa.create_engine(url)
    try:
        with engine.connect() as conn:
            conn.execute(sa.text("SELECT 1"))
    except Exception as e:
        raise ConnectionError(f"Failed to connect to the database: {e}")
    return engine


def create_session(engine: Optional[sa.Engine] = None, db_type: str = "sqlite") -> sessionmaker:
    """Create SQLAlchemy session factory."""
    if engine is None:
        engine = create_engine(db_type)
    return sessionmaker(bind=engine)
