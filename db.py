"""Database connection - falls back to CSVs on Streamlit Cloud."""

import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# Cache for CSV fallback
_csv_cache = {}


def run_query(sql: str) -> pd.DataFrame:
    """Run a query or fall back to CSV files if PostgreSQL is not available."""
    try:
        # Try PostgreSQL first (local)
        from sqlalchemy import create_engine
        host = os.getenv("DB_HOST", "localhost")
        port = os.getenv("DB_PORT", "5432")
        name = os.getenv("DB_NAME", "inditex_db")
        user = os.getenv("DB_USER", "postgres")
        password = os.getenv("DB_PASSWORD", "postgres")
        url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"
        engine = create_engine(url)
        return pd.read_sql(sql, engine)
    except Exception:
        # Fall back to CSVs
        return _query_from_csv(sql)


def _query_from_csv(sql: str) -> pd.DataFrame:
    """Simple CSV fallback for common queries on Streamlit Cloud."""
    sql_lower = sql.lower().strip()

    # Identify which tables are needed
    tables = []
    if "brands" in sql_lower:
        tables.append("brands")
    if "sales_by_brand" in sql_lower:
        tables.append("sales_by_brand")
    if "financials" in sql_lower:
        tables.append("financials")
    if "sales_by_region" in sql_lower:
        tables.append("sales_by_region")

    # Load CSVs (cached)
    dfs = {}
    for t in tables:
        if t not in _csv_cache:
            _csv_cache[t] = pd.read_csv(f"{t}.csv")
        dfs[t] = _csv_cache[t]

    # Simple cases
    if "brands" in dfs and "sales_by_brand" in dfs and "join" in sql_lower:
        result = dfs["sales_by_brand"].merge(
            dfs["brands"], on="brand_id"
        ).sort_values("sales_millions", ascending=False)
        return result

    if "financials" in dfs and "brands" not in dfs and "sales" not in dfs:
        return dfs["financials"].sort_values("year")

    if "sales_by_region" in dfs:
        return dfs["sales_by_region"].sort_values("sales_pct", ascending=False)

    if "brands" in dfs:
        return dfs["brands"].sort_values("brand_id")

    return pd.DataFrame()
