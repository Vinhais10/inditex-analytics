"""
Inditex Analytics — Elite Natural Language SQL Agent.

Features:
- Few-shot examples (EN / PT / ES)
- Chain of Thought reasoning (explicit plan before SQL)
- SQL validation (blocks anything that is not a SELECT/WITH)
- Auto-retry with error feedback (up to 2 attempts)
- Query logging (all queries saved to query_log table)
- Follow-up suggestions
- Multi-language: auto-detects EN / PT / ES and replies in that language
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
MODEL = "llama-3.3-70b-versatile"


# ============================================================
# SYSTEM PROMPT — global, defines identity and language rules
# ============================================================
SYSTEM_PROMPT = """You are a senior data analyst agent for Inditex (Zara, Bershka, Stradivarius, Massimo Dutti, Pull&Bear, Oysho).

LANGUAGE RULES (highest priority):
- Detect the language of the user's question.
- If the question is in English, answer in English.
- If the question is in Portuguese, answer in Portuguese (pt-PT).
- If the question is in Spanish, answer in Spanish (es-ES).
- If the question is mixed or unclear, default to English.
- ALWAYS write SQL, table names, and column names in English (the schema is in English).
- Follow-up suggestions must be in the same language as the question.

STYLE:
- Professional, concise, business-oriented.
- Never invent data. Only use the schema provided.
"""


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


# ============================================================
# FEW-SHOT — EN / PT / ES
# ============================================================
FEW_SHOT = """
Example 1 (PT):
Q: Qual é a marca mais rentável?
SQL: SELECT b.brand_name, s.sales_millions FROM sales_by_brand s JOIN brands b ON s.brand_id = b.brand_id ORDER BY s.sales_millions DESC LIMIT 1;

Example 2 (PT):
Q: Como evoluiu a receita entre 2023 e 2025?
SQL: SELECT year, revenue_millions FROM financials ORDER BY year;

Example 3 (PT):
Q: Que região representa mais de 50% das vendas?
SQL: SELECT region, sales_pct FROM sales_by_region WHERE sales_pct > 50 ORDER BY sales_pct DESC;

Example 4 (PT):
Q: Qual é a marca que cresce mais rápido?
SQL: SELECT b.brand_name, s.growth_pct FROM sales_by_brand s JOIN brands b ON s.brand_id = b.brand_id ORDER BY s.growth_pct DESC LIMIT 1;

Example 5 (PT):
Q: Quantas lojas tinha em 2025?
SQL: SELECT stores_count FROM financials WHERE year = 2025;

Example 6 (EN):
Q: Which brand is growing fastest?
SQL: SELECT b.brand_name, s.growth_pct FROM sales_by_brand s JOIN brands b ON s.brand_id = b.brand_id ORDER BY s.growth_pct DESC LIMIT 1;

Example 7 (ES):
Q: ¿Qué marca está creciendo más rápido?
SQL: SELECT b.brand_name, s.growth_pct FROM sales_by_brand s JOIN brands b ON s.brand_id = b.brand_id ORDER BY s.growth_pct DESC LIMIT 1;

Example 8 (ES):
Q: ¿Cuál es el margen de beneficio en 2025?
SQL: SELECT gross_margin_pct FROM financials WHERE year = 2025;
"""


# ============================================================
# LANGUAGE DETECTION
# ============================================================
def detect_language(text: str) -> str:
    """Return 'en', 'pt' or 'es'. Defaults to 'en' when unsure."""
    t = text.lower()

    pt_markers = [
        "qual", "quais", "como", "quanto", "quantos", "quantas",
        "que ", "onde", "quando", "porque", "porquê",
        "marca", "região", "regiao", "vendas", "receita",
        "cresce", "crescimento", "lucro", "margem", "lojas", "ano",
        "é ", "são", "está", "estão", "foi", "eram",
    ]
    es_markers = [
        "cuál", "cual", "cómo", "como ", "cuánto", "cuántos", "cuántas",
        "qué", "donde", "cuándo", "por qué",
        "marca", "región", "ventas", "ingresos",
        "crece", "crecimiento", "beneficio", "margen", "tiendas", "año",
        "está", "están", "fue", "eran", "más",
    ]

    pt_score = sum(1 for m in pt_markers if m in t)
    es_score = sum(1 for m in es_markers if m in t)

    # Accents are strong signals
    if any(c in t for c in "ãõçáéíóúâêôà"):
        pt_score += 2
    if any(c in t for c in "ñ¿¡áéíóú"):
        es_score += 2

    if pt_score > es_score and pt_score > 0:
        return "pt"
    if es_score > pt_score and es_score > 0:
        return "es"
    return "en"


# ============================================================
# STEP 1 — PLAN
# ============================================================
def generate_plan(question: str, lang: str) -> str:
    prompt = f"""{SCHEMA}

The user asked (language={lang}): "{question}"

Before writing SQL, think step by step:
1. Which tables are needed?
2. Do we need JOINs?
3. What filters (WHERE)?
4. What ordering (ORDER BY)?
5. How many rows (LIMIT)?

Output a concise plan (3-5 bullet points max). Do NOT write SQL yet.
Answer in the same language as the question ({lang}).
"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
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
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
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
        pass


# ============================================================
# STEP 5 — EXPLAIN
# ============================================================
def explain_result(question: str, sql: str, result, lang: str) -> str:
    result_str = result.to_string(index=False) if not result.empty else "(no results)"

    prompt = f"""The user asked (language={lang}): "{question}"

SQL:
{sql}

Result:
{result_str}

Write:
1. A direct answer (1-2 sentences).
2. A business insight (1 sentence).

Answer in language={lang}. Be professional and precise.
"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()


# ============================================================
# STEP 6 — FOLLOW-UP SUGGESTIONS
# ============================================================
def suggest_followups(question: str, result, lang: str) -> list[str]:
    result_str = result.to_string(index=False) if not result.empty else "(empty)"

    prompt = f"""The user asked (language={lang}): "{question}"

The result was:
{result_str}

Suggest 3 short, interesting follow-up questions the user might want to ask next.
Rules:
- Return ONLY a bullet list with 3 items, no preamble, no explanation.
- Use language={lang}.
- Each question must be answerable from the same database.
"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.5,
    )

    text = response.choices[0].message.content.strip()
    lines = [l.strip("- •*").strip() for l in text.split("\n") if l.strip()]
    return [l for l in lines if l][:3]


# ============================================================
# MAIN
# ============================================================
def ask(question: str, verbose: bool = False) -> dict:
    lang = detect_language(question)
    if verbose:
        print(f"[agent] detected language: {lang}")

    plan = generate_plan(question, lang)
    execution = execute_with_retry(question, plan)

    if not execution["success"]:
        error_msgs = {
            "pt": f"⚠️ Não consegui responder. Erro: {execution['error']}",
            "es": f"⚠️ No pude responder. Error: {execution['error']}",
            "en": f"⚠️ I could not answer. Error: {execution['error']}",
        }
        return {
            "plan": plan,
            "sql": execution["sql"],
            "error": execution["error"],
            "attempts": execution["attempts"],
            "explanation": error_msgs.get(lang, error_msgs["en"]),
            "language": lang,
        }

    result = execution["result"]
    explanation = explain_result(question, execution["sql"], result, lang)
    followups = suggest_followups(question, result, lang)

    return {
        "plan": plan,
        "sql": execution["sql"],
        "result": result,
        "explanation": explanation,
        "followups": followups,
        "attempts": execution["attempts"],
        "duration_ms": execution.get("duration_ms"),
        "language": lang,
    }
