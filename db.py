"""Database connection helper for the Inditex Analytics dashboard."""

import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()


def get_engine():
    """Create a SQLAlchemy engine from .env variables."""
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    name = os.getenv("DB_NAME", "inditex_db")
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", "postgres")

    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"
    return create_engine(url)


def run_query(sql: str) -> pd.DataFrame:
    """Run a SQL query and return the result as a DataFrame."""
    engine = get_engine()
    return pd.read_sql(sql, engine)
