"""
Inditex Analytics — Elite Natural Language SQL Agent.

Features:
- Few-shot examples for higher SQL accuracy
- Chain of Thought reasoning (explicit plan before SQL)
- SQL validation (blocks anything that is not a SELECT/WITH)
- Auto-retry with error feedback (up to 2 attempts)
- Query logging (all queries saved to query_log table)
- Follow-up suggestions
"""

import os
import re
import time
from dotenv import load_dotenv
from groq import Groq

from db import run_query, get_engine

load_dotenv()


def _get_groq_key():
    key = os.getenv("GROQ_API_KEY")
    if not key:
        raise RuntimeError("GROQ_API_KEY not found in .env")
    return key


client = Groq(api_key=_get_groq_key())
MODEL = "openai/gpt-oss-120b"


# ============================================================
# SCHEMA
# ============================================================
SCHEMA = """
PostgreSQL database schema:

Table: brands
  brand_id (integer, PK)
  brand_name (varchar)

Table: sales_by_brand
  id (integer, PK)
  brand_id (integer, FK -> brands.brand_id)
  year (integer)
  sales_millions (numeric)
  growth_pct (numeric, YoY % growth)

Table: sales_by_region
  id (integer, PK)
  region (varchar) — 'Europe (excl. Spain)', 'Americas', 'Spain', 'Asia & Rest of World'
  year (integer)
  sales_pct (numeric)

Table: financials
  id (integer, PK)
  year (integer, unique)
  revenue_millions (numeric)
  net_income_millions (numeric)
  gross_margin_pct (numeric)
  stores_count (integer)
  countries_count (integer)

Data covers years 2023, 2024, 2025.
"""


FEW_SHOT = """
Example 1:
Q: Qual é a marca mais rentável?
SQL: SELECT b.brand_name, s.sales_millions FROM sales_by_brand s JOIN brands b ON s.brand_id = b.brand_id ORDER BY s.sales_millions DESC LIMIT 1;

Example 2:
Q: Como evoluiu a receita entre 2023 e 2025?
SQL: SELECT year, revenue_millions FROM financials ORDER BY year;

Example 3:
Q: Que região representa mais de 50% das vendas?
SQL: SELECT region, sales_pct FROM sales_by_region WHERE sales_pct > 50 ORDER BY sales_pct DESC;

Example 4:
Q: Qual é a marca que cresce mais rápido?
SQL: SELECT b.brand_name, s.growth_pct FROM sales_by_brand s JOIN brands b ON s.brand_id = b.brand_id ORDER BY s.growth_pct DESC LIMIT 1;

Example 5:
Q: Quantas lojas tinha em 2025?
SQL: SELECT stores_count FROM financials WHERE year = 2025;
"""


# ============================================================
# STEP 1 — PLAN
# ============================================================
def generate_plan(question: str) -> str:
    prompt = f"""{SCHEMA}

The user asked: "{question}"

Before writing SQL, think step by step:
1. Which tables are needed?
2. Do we need JOINs?
3. What filters (WHERE)?
4. What ordering (ORDER BY)?
5. How many rows (LIMIT)?

Output a concise plan (3-5 bullet points max). Do NOT write SQL yet.
Answer in the same language as the question.
"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()


# ============================================================
# STEP 2 — SQL
# ============================================================
def generate_sql(question: str, plan: str, previous_error: str = None) -> str:
    extra = ""
    if previous_error:
        extra = f"""
The previous attempt failed with this error:
{previous_error}

Fix the SQL and try again. Think carefully about column names and table names.
"""

    prompt = f"""{SCHEMA}

{FEW_SHOT}

The user asked: "{question}"

Here is the plan:
{plan}
{extra}

Write a single valid PostgreSQL query that answers the question.
Rules:
- Output ONLY the SQL. No explanation, no markdown, no code fences.
- Only SELECT or WITH statements. Never INSERT, UPDATE, DELETE, DROP.
- End with a semicolon.
"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
    )

    sql = response.choices[0].message.content.strip()
    if sql.startswith("```"):
        sql = sql.split("```")[1]
        if sql.lower().startswith("sql"):
            sql = sql[3:]
        sql = sql.strip()

    return sql


# ============================================================
# STEP 3 — VALIDATE
# ============================================================
FORBIDDEN = [
    "INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE",
    "TRUNCATE", "GRANT", "REVOKE", "EXEC", "EXECUTE",
]


def validate_sql(sql: str) -> tuple[bool, str]:
    cleaned = sql.strip().rstrip(";").strip().upper()

    if not (cleaned.startswith("SELECT") or cleaned.startswith("WITH")):
        return False, "Only SELECT or WITH queries are allowed."

    for kw in FORBIDDEN:
        if re.search(rf"\b{kw}\b", cleaned):
            return False, f"Forbidden keyword: {kw}"

    if ";" in sql.strip().rstrip(";"):
        return False, "Multiple statements are not allowed."

    return True, "OK"


# ============================================================
# STEP 4 — EXECUTE WITH RETRY
# ============================================================
def execute_with_retry(question: str, plan: str, max_attempts: int = 2) -> dict:
    """Try to execute SQL. If it fails, ask the LLM to fix it."""
    sql = generate_sql(question, plan)
    last_error = None

    for attempt in range(1, max_attempts + 1):
        is_valid, reason = validate_sql(sql)
        if not is_valid:
            return {
                "sql": sql,
                "error": reason,
                "attempts": attempt,
                "success": False,
            }

        try:
            start = time.time()
            result = run_query(sql)
            duration_ms = int((time.time() - start) * 1000)

            _log_query(question, sql, True, None, duration_ms)

            return {
                "sql": sql,
                "result": result,
                "attempts": attempt,
                "duration_ms": duration_ms,
                "success": True,
            }
        except Exception as e:
            last_error = str(e)
            if attempt < max_attempts:
                # Ask LLM to fix the SQL
                sql = generate_sql(question, plan, previous_error=last_error)
            else:
                _log_query(question, sql, False, last_error, None)
                return {
                    "sql": sql,
                    "error": last_error,
                    "attempts": attempt,
                    "success": False,
                }

    return {"sql": sql, "error": "Max attempts reached", "attempts": max_attempts, "success": False}


# ============================================================
# LOGGING
# ============================================================
def _log_query(question: str, sql: str, success: bool, error: str, duration_ms: int):
    """Save query to query_log table. Silent fail if it doesn't work."""
    try:
        engine = get_engine()
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(
                text("""
                    INSERT INTO query_log (question, sql, success, error_message, duration_ms)
                    VALUES (:q, :s, :ok, :err, :dur)
                """),
                {"q": question, "s": sql, "ok": success, "err": error, "dur": duration_ms},
            )
            conn.commit()
    except Exception:
        pass  # Never break the main flow because of logging


# ============================================================
# STEP 5 — EXPLAIN
# ============================================================
def explain_result(question: str, sql: str, result) -> str:
    result_str = result.to_string(index=False) if not result.empty else "(sem resultados)"

    prompt = f"""The user asked: "{question}"

SQL:
{sql}

Result:
{result_str}

Write:
1. A direct answer (1-2 sentences).
2. A business insight (1 sentence).

Same language as the question. Be professional and precise.
"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()


# ============================================================
# STEP 6 — FOLLOW-UP SUGGESTIONS
# ============================================================
def suggest_followups(question: str, result) -> list[str]:
    result_str = result.to_string(index=False) if not result.empty else "(vazio)"

    prompt = f"""The user asked: "{question}"

The result was:
{result_str}

Suggest 3 short, interesting follow-up questions the user might want to ask next.
Rules:
- Return ONLY a bullet list with 3 items, no preamble, no explanation.
- Use the same language as the question.
- Each question must be answerable from the same database.
"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )

    text = response.choices[0].message.content.strip()
    lines = [l.strip("- •*").strip() for l in text.split("\n") if l.strip()]
    return [l for l in lines if l][:3]


# ============================================================
# MAIN
# ============================================================
def ask(question: str, verbose: bool = False) -> dict:
    plan = generate_plan(question)
    execution = execute_with_retry(question, plan)

    if not execution["success"]:
        return {
            "plan": plan,
            "sql": execution["sql"],
            "error": execution["error"],
            "attempts": execution["attempts"],
            "explanation": f"⚠️ Não consegui responder. Erro: {execution['error']}",
        }

    result = execution["result"]
    explanation = explain_result(question, execution["sql"], result)
    followups = suggest_followups(question, result)

    return {
        "plan": plan,
        "sql": execution["sql"],
        "result": result,
        "explanation": explanation,
        "followups": followups,
        "attempts": execution["attempts"],
        "duration_ms": execution.get("duration_ms"),
    }



