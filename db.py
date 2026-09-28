"""Database connection - falls back to CSVs on Streamlit Cloud."""

import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

_csv_cache = {}


def run_query(sql: str) -> pd.DataFrame:
    """Run SQL on PostgreSQL, or fall back to CSV files on Streamlit Cloud."""
    try:
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
        return _query_from_csv(sql)


def _query_from_csv(sql: str) -> pd.DataFrame:
    """Simple CSV fallback for the dashboards queries."""
    sql_lower = sql.lower().strip()

    needed = []
    for table in ["brands", "sales_by_brand", "sales_by_region", "financials"]:
        if table in sql_lower:
            needed.append(table)

    dfs = {}
    for t in needed:
        if t not in _csv_cache:
            _csv_cache[t] = pd.read_csv(f"{t}.csv")
        dfs[t] = _csv_cache[t]

    if "sales_by_brand" in dfs and "brands" in dfs:
        merged = dfs["sales_by_brand"].merge(dfs["brands"], on="brand_id")
        return merged.sort_values("sales_millions", ascending=False)

    if "sales_by_region" in dfs:
        return dfs["sales_by_region"].sort_values("sales_pct", ascending=False)

    if "financials" in dfs and "brands" not in dfs and "sales" not in dfs:
        return dfs["financials"].sort_values("year")

    if "brands" in dfs:
        return dfs["brands"].sort_values("brand_id")

    return pd.DataFrame()
