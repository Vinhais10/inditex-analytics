"""Database connection - falls back to CSVs on Streamlit Cloud."""

import os
import re
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
    """Simple CSV fallback that respects basic WHERE and ORDER BY."""
    sql_lower = sql.lower().strip()

    # 1) Descobrir que tabelas precisa
    needed = []
    for table in ["brands", "sales_by_brand", "sales_by_region", "financials"]:
        if table in sql_lower:
            needed.append(table)

    # 2) Carregar tabelas (com cache)
    dfs = {}
    for t in needed:
        if t not in _csv_cache:
            _csv_cache[t] = pd.read_csv(f"{t}.csv")
        dfs[t] = _csv_cache[t].copy()

    # 3) Aplicar WHERE simples (year = X)
    year_match = re.search(r"where\s+.*?\.?year\s*=\s*(\d{4})", sql_lower)
    if year_match:
        year_filter = int(year_match.group(1))
        for t in list(dfs.keys()):
            if "year" in dfs[t].columns:
                dfs[t] = dfs[t][dfs[t]["year"] == year_filter]

    # 4) Aplicar JOIN (brands + sales_by_brand)
    if "sales_by_brand" in dfs and "brands" in dfs:
        merged = dfs["sales_by_brand"].merge(dfs["brands"], on="brand_id")

        # Ordenar
        if "order by" in sql_lower:
            if "growth_pct" in sql_lower and "desc" in sql_lower:
                merged = merged.sort_values("growth_pct", ascending=False)
            elif "growth_pct" in sql_lower and "asc" in sql_lower:
                merged = merged.sort_values("growth_pct", ascending=True)
            elif "sales_millions" in sql_lower and "asc" in sql_lower:
                merged = merged.sort_values("sales_millions", ascending=True)
            else:
                merged = merged.sort_values("sales_millions", ascending=False)

        # LIMIT
        limit_match = re.search(r"limit\s+(\d+)", sql_lower)
        if limit_match:
            merged = merged.head(int(limit_match.group(1)))

        # Selecionar colunas pedidas
        if "growth_pct" in sql_lower and "sales_millions" in sql_lower:
            return merged[["brand_name", "sales_millions", "growth_pct"]]
        if "growth_pct" in sql_lower:
            return merged[["brand_name", "growth_pct"]]
        return merged[["brand_name", "sales_millions"]]

    # 5) sales_by_region
    if "sales_by_region" in dfs:
        df = dfs["sales_by_region"]
        if "order by" in sql_lower and "year" in sql_lower:
            df = df.sort_values(["year", "region"])
        else:
            df = df.sort_values("sales_pct", ascending=False)
        return df

    # 6) financials
    if "financials" in dfs:
        return dfs["financials"].sort_values("year")

    # 7) brands
    if "brands" in dfs:
        return dfs["brands"].sort_values("brand_id")

    return pd.DataFrame()
