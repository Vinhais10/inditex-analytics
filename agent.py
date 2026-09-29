"""
Inditex Analytics - Elite Natural Language SQL Agent.
"""

import os
import re
import time
from dotenv import load_dotenv
from groq import Groq

from db import run_query

load_dotenv()


def _get_groq_key():
    key = os.getenv("GROQ_API_KEY")
    if not key:
        raise RuntimeError("GROQ_API_KEY not found in .env")
    return key


# Cloudflare AI Gateway (proxy para Groq)
CF_ACCOUNT_ID = "ba5cb58ffe90179fc0401413385fcafa"
CF_GATEWAY_ID = "inditex-gateway"

client = Groq(
    api_key=_get_groq_key(),
    base_url=f"https://gateway.ai.cloudflare.com/v1/{CF_ACCOUNT_ID}/{CF_GATEWAY_ID}/groq"
)
MODEL = "openai/gpt-oss-120b"


SYSTEM_PROMPT = """You are a senior data analyst agent for Inditex (Zara, Bershka, Stradivarius, Massimo Dutti, Pull&Bear, Oysho).

LANGUAGE RULES (highest priority):
- Detect the language of the user's question.
- If the question is in English, answer in English.
- If the question is in Portuguese, answer in Portuguese (pt-PT).
- If the question is in Spanish, answer in Spanish (es-ES).
- If the question is mixed or unclear, default to English.
- ALWAYS write SQL, table names, and column names in English.
- Follow-up suggestions must be in the same language as the question.

CONVERSATION CONTEXT:
- You may receive previous messages in the conversation.
- If the user asks a follow-up question (e.g., "and the year before?", "e no ano anterior?", "y el año anterior?"), use the previous conversation to understand WHAT they are asking about.
- Example: if the previous answer was about a BRAND, the follow-up "and the year before?" also refers to BRANDS (not regions).
- Do NOT switch topics unless the user explicitly changes them.

STYLE:
- Professional, concise, business-oriented.
- Never invent data. Only use the schema provided.
- If a question requires data from two different tables, run TWO queries or use UNION ALL.
- Never answer "no data available" without first trying multiple queries.

MARKET SHARE / CUOTA DE MERCADO RULES:
- sales_by_region.sales_pct IS ALREADY the market share for that region-year.
- For BRANDS, share = sales_millions / SUM(sales_millions) for that year.
- "Ganar cuota de mercado" = sales_pct INCREASED from 2023 to 2025.
- "Perder peso relativo" = brand share DECREASED from 2023 to 2025.

DATA AVAILABILITY:
- financials: 2023, 2024, 2025
- sales_by_brand: 2023, 2024, 2025
- sales_by_region: 2023, 2024, 2025
"""


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
  region (varchar) - 'Europe (excl. Spain)', 'Americas', 'Spain', 'Asia & Rest of World'
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
Example 1 (PT):
Q: Qual e a marca mais rentavel?
SQL: SELECT b.brand_name, s.sales_millions FROM sales_by_brand s JOIN brands b ON s.brand_id = b.brand_id WHERE s.year = 2025 ORDER BY s.sales_millions DESC LIMIT 1;

Example 2 (PT):
Q: Como evoluiu a receita entre 2023 e 2025?
SQL: SELECT year, revenue_millions FROM financials ORDER BY year;

Example 3 (PT):
Q: Qual e a marca que cresce mais rapido?
SQL: SELECT b.brand_name, s.growth_pct FROM sales_by_brand s JOIN brands b ON s.brand_id = b.brand_id WHERE s.year = 2025 ORDER BY s.growth_pct DESC LIMIT 1;

Example 4 (PT) - FOLLOW-UP:
Previous: Qual e a marca que cresce mais rapido? (answer: Oysho)
Q: E no ano anterior?
SQL: SELECT b.brand_name, s.growth_pct FROM sales_by_brand s JOIN brands b ON s.brand_id = b.brand_id WHERE s.year = 2024 ORDER BY s.growth_pct DESC LIMIT 1;

Example 5 (EN):
Q: Which brand is growing fastest?
SQL: SELECT b.brand_name, s.growth_pct FROM sales_by_brand s JOIN brands b ON s.brand_id = b.brand_id WHERE s.year = 2025 ORDER BY s.growth_pct DESC LIMIT 1;

Example 6 (ES):
Q: Que marca esta creciendo mas rapido?
SQL: SELECT b.brand_name, s.growth_pct FROM sales_by_brand s JOIN brands b ON s.brand_id = b.brand_id WHERE s.year = 2025 ORDER BY s.growth_pct DESC LIMIT 1;

Example 7 (ES) - MARKET SHARE REGIONS:
Q: Que region gano mas cuota de mercado entre 2023 y 2025?
SQL: SELECT r23.region, r23.sales_pct AS pct_2023, r25.sales_pct AS pct_2025, (r25.sales_pct - r23.sales_pct) AS cambio FROM sales_by_region r23 JOIN sales_by_region r25 ON r23.region = r25.region WHERE r23.year = 2023 AND r25.year = 2025 ORDER BY cambio DESC;

Example 8 (ES) - MARKET SHARE BRANDS:
Q: Que marca perdio mas peso relativo entre 2023 y 2025?
SQL: WITH shares AS (SELECT b.brand_name, s.year, s.sales_millions * 100.0 / SUM(s.sales_millions) OVER (PARTITION BY s.year) AS share FROM sales_by_brand s JOIN brands b ON s.brand_id = b.brand_id) SELECT a.brand_name, a.share AS share_2023, c.share AS share_2025, (c.share - a.share) AS cambio FROM shares a JOIN shares c ON a.brand_name = c.brand_name WHERE a.year = 2023 AND c.year = 2025 ORDER BY cambio ASC LIMIT 1;
"""


def detect_language(text: str) -> str:
    t = " " + text.lower().strip() + " "

    pt_strong = [
        " qual", " quais", " quanto", " quantos", " quantas",
        " onde", " quando", " porque",
        "regiao", "vendas", "receita", "lucro",
        "cresce ", "cresceu", "crescimento",
        "lojas", "sao ", "estao ", "eram",
        " e a marca", " e o ", " e a ",
        "nao ", "mais rapido", "mais rapida", "mais rentavel",
        "melhor marca", "melhor ", "pior ",
        "quantas lojas", "que regiao",
        " como ", " como?",
        "tens", "temos", "certo", "informacao",
        "dados", " so ", "apenas", "existe", "ha ",
        "podes", "queres", "quero", "tambem",
        "entao", "verdade",
    ]
    es_strong = [
        "cual ", "cuales ", "cuanto", "cuantos", "cuantas",
        " donde", " cuando",
        "region", "ventas", "ingresos", "beneficio",
        "crece ", "crecio", "crecimiento",
        "tiendas", "estan ",
        " es la marca", " es el ", " es la ", " es mejor",
        " mas rapido", " mas rapida", " mas rentable",
        "mejor marca", "mejor ", "peor ",
        "que marca", "que region",
        " como ", " como?",
        "tienes", "tenemos", "cierto", "informacion",
        "datos", " solo ", "existe", "hay ",
        "puedes", "quieres", "quiero", "tambien",
        "entonces", "verdad",
        "cuota", "peso relativo",
    ]
    shared_pt_es = [
        "marca", "ano", "region", "margen", "margem",
        "loja", "tienda", "venda", "venta",
    ]
    en_strong = [
        "which ", "what ", "how ", "where ", "when ", "why ",
        " is ", " are ", " the ", " of ", " in ", " for ",
        "brand", "region", "sales", "revenue", "profit",
        "grow", "growing", "growth", "margin",
        "stores", "countries", "year",
        "fastest", "most", "biggest", "best", "top ",
        "does ", "do ", "did ", "was ", "were ",
        "market share", "share", "gained", "lost",
    ]

    pt_score = es_score = en_score = 0

    for m in pt_strong:
        if m in t: pt_score += 2
    for m in es_strong:
        if m in t: es_score += 2
    for m in shared_pt_es:
        if m in t:
            pt_score += 1
            es_score += 1
    for m in en_strong:
        if m in t: en_score += 1

    if any(c in t for c in "\u00e3\u00f5\u00e7"): pt_score += 4
    if any(c in t for c in "\u00f1\u00bf\u00a1"): es_score += 4
    if any(c in t for c in "\u00e1\u00e9\u00ed\u00f3\u00fa\u00e2\u00ea\u00f4"):
        pt_score += 1
        es_score += 1

    scores = {"pt": pt_score, "es": es_score, "en": en_score}
    best = max(scores, key=scores.get)
    if scores[best] == 0: return "en"
    return best


def _build_messages(prompt: str, history: list = None) -> list:
    """Build messages with system prompt + history + new prompt."""
    msgs = [{"role": "system", "content": SYSTEM_PROMPT}]
    if history:
        for h in history[-6:]:
            role = h.get("role", "user")
            content = h.get("content", "")
            if role in ("user", "assistant") and content:
                msgs.append({"role": role, "content": content})
    msgs.append({"role": "user", "content": prompt})
    return msgs


def generate_plan(question: str, lang: str, history: list = None) -> str:
    prompt = f"""{SCHEMA}

The user asked (language={lang}): "{question}"

Before writing SQL, think step by step:
1. Which tables are needed? (1, 2, or 3)
2. Do we need JOINs?
3. What filters (WHERE)?
4. What ordering (ORDER BY)?
5. Is this a follow-up to a previous question? If so, which topic is it about?

Output a concise plan (3-5 bullet points max). Do NOT write SQL yet.
Answer in the same language as the question ({lang}).
"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=_build_messages(prompt, history),
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()


def generate_sql(question: str, plan: str, previous_error: str = None, history: list = None) -> str:
    extra = ""
    if previous_error:
        extra = f"""
The previous attempt failed with this error:
{previous_error}

Fix the SQL and try again. Think carefully about column names and table names.
If the result was empty, try a DIFFERENT approach (different JOIN, subquery, or UNION).
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
- If the question needs data from multiple unrelated tables, use UNION ALL with a label column.
"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=_build_messages(prompt, history),
        temperature=0.1,
    )

    sql = response.choices[0].message.content.strip()
    if sql.startswith("```"):
        sql = sql.split("```")[1]
        if sql.lower().startswith("sql"):
            sql = sql[3:]
        sql = sql.strip()

    return sql


FORBIDDEN = [
    "INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE",
    "TRUNCATE", "GRANT", "REVOKE", "EXEC", "EXECUTE",
]


def validate_sql(sql: str) -> tuple:
    cleaned = sql.strip().rstrip(";").strip().upper()
    if not (cleaned.startswith("SELECT") or cleaned.startswith("WITH")):
        return False, "Only SELECT or WITH queries are allowed."
    for kw in FORBIDDEN:
        if re.search(rf"\b{kw}\b", cleaned):
            return False, f"Forbidden keyword: {kw}"
    if ";" in sql.strip().rstrip(";"):
        return False, "Multiple statements are not allowed."
    return True, "OK"


def execute_with_retry(question: str, plan: str, history: list = None, max_attempts: int = 3) -> dict:
    sql = generate_sql(question, plan, history=history)
    last_error = None

    for attempt in range(1, max_attempts + 1):
        is_valid, reason = validate_sql(sql)
        if not is_valid:
            return {"sql": sql, "error": reason, "attempts": attempt, "success": False}

        try:
            start = time.time()
            result = run_query(sql)
            duration_ms = int((time.time() - start) * 1000)

            if result.empty and attempt < max_attempts:
                last_error = "Query returned empty result. Try a different approach."
                sql = generate_sql(question, plan, previous_error=last_error, history=history)
                continue

            _log_query(question, sql, True, None, duration_ms)
            return {
                "sql": sql, "result": result, "attempts": attempt,
                "duration_ms": duration_ms, "success": True,
            }
        except Exception as e:
            last_error = str(e)
            if attempt < max_attempts:
                sql = generate_sql(question, plan, previous_error=last_error, history=history)
            else:
                _log_query(question, sql, False, last_error, None)
                return {"sql": sql, "error": last_error, "attempts": attempt, "success": False}

    return {"sql": sql, "error": "Max attempts reached", "attempts": max_attempts, "success": False}


def _log_query(question: str, sql: str, success: bool, error: str, duration_ms: int):
    try:
        import db as _db
        get_engine = getattr(_db, "get_engine", None)
        if get_engine is None:
            return
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


def explain_result(question: str, sql: str, result, lang: str, history: list = None) -> str:
    result_str = result.to_string(index=False) if not result.empty else "(no results)"

    prompt = f"""The user asked (language={lang}): "{question}"

SQL:
{sql}

Result:
{result_str}

Write:
1. A direct answer (1-2 sentences).
2. A business insight (1 sentence).

CRITICAL: Write your entire answer in language={lang}.
If this is a follow-up, refer to the previous topic correctly.
"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=_build_messages(prompt, history),
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()


def suggest_followups(question: str, result, lang: str) -> list:
    result_str = result.to_string(index=False) if not result.empty else "(empty)"

    prompt = f"""The user asked (language={lang}): "{question}"

The result was:
{result_str}

Suggest 3 short follow-up questions the user might want to ask next.
Rules:
- Return ONLY a bullet list with 3 items.
- Write the follow-ups in language={lang}.
- Each question must be answerable from the same database.
"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=_build_messages(prompt),
        temperature=0.5,
    )

    text = response.choices[0].message.content.strip()
    lines = [l.strip("- *").strip() for l in text.split("\n") if l.strip()]
    return [l for l in lines if l][:3]


def ask(question: str, verbose: bool = False, history: list = None) -> dict:
    lang = detect_language(question)
    if verbose:
        print(f"[agent] detected language: {lang}")

    plan = generate_plan(question, lang, history=history)
    execution = execute_with_retry(question, plan, history=history)

    if not execution["success"]:
        error_msgs = {
            "pt": f"Erro: {execution['error']}",
            "es": f"Error: {execution['error']}",
            "en": f"Error: {execution['error']}",
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
    explanation = explain_result(question, execution["sql"], result, lang, history=history)
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


