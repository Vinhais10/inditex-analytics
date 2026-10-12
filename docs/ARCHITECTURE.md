# Architecture

Technical deep-dive into how Inditex Analytics is built.

---

## System Overview

    +---------------------+
    |   PostgreSQL 17     |
    |   inditex_db        |
    |---------------------|
    |   brands            |
    |   sales_by_brand    |
    |   sales_by_region   |
    |   financials        |
    |   query_log         |
    +----------+----------+
               |
               | (psycopg2 + SQLAlchemy)
               |
    +----------+----------+-------------------+
    |                     |                   |
    v                     v                   v
+---------+         +----------+        +-----------+
|   CLI   |         |  Data    |        | Dashboard |
| Typer + |         |  Agent   |        | Streamlit |
|  Rich   |         | Groq LLM |        | + Plotly  |
+---------+         +----------+        +-----------+
    |                     |                   |
    +---------------------+-------------------+
                          |
                    +-----+-----+
                    |  db.py    |
                    | shared    |
                    | interface |
                    +-----------+

---

## Components

### 1. PostgreSQL Database

**Tables:**

- **brands** — Zara, Bershka, Stradivarius, Massimo Dutti, Pull&Bear, Oysho
- **sales_by_brand** — Sales per brand per year, with YoY growth
- **sales_by_region** — Sales distribution by geographic region
- **financials** — Revenue, net income, gross margin, stores, countries per year
- **query_log** — Audit trail of all agent queries

**Schema design principles:**

- Primary keys on every table
- Foreign key from sales_by_brand.brand_id to brands.brand_id
- Unique constraint on financials.year
- Indexes on frequently joined columns

### 2. Shared Database Interface (db.py)

Single point of access for all components:

    from db import run_query
    df = run_query("SELECT * FROM brands")

- Uses SQLAlchemy engine
- Reads connection parameters from .env
- Returns pandas DataFrames
- Zero duplication across CLI, agent, and dashboard

### 3. Professional CLI (cli.py)

Built with **Typer** (command framework) and **Rich** (terminal formatting).

**Commands:**

| Command | Purpose |
|---|---|
| report | Financial report for a given year |
| brands | Sales and growth by brand |
| abc | ABC analysis of brand portfolio |
| regions | Geographic sales distribution |
| growth | Growth ranking with medals |
| ask | Natural language query (Data Agent) |

**Why Typer?**

- Auto-generated help pages
- Type-safe arguments
- Simple to extend

**Why Rich?**

- Beautiful tables
- Progress spinners
- Colored output
- Panels and layout

### 4. Data Agent (agent.py)

An AI agent that converts natural language into SQL and explains results.

**Pipeline (7 steps):**

    Question (any language)
         |
    1. PLAN      -- LLM reasons about the approach
         |
    2. GENERATE  -- LLM writes SQL (few-shot examples)
         |
    3. VALIDATE  -- Block non-SELECT/WITH queries
         |
    4. EXECUTE   -- Run in PostgreSQL
         |
    5. RETRY     -- If it fails, LLM receives the error and fixes it
         |
    6. EXPLAIN   -- Natural language answer + insight
         |
    7. SUGGEST   -- 3 follow-up questions
         |
    Final result

**Safety features:**

- SQL validation blocks INSERT, UPDATE, DELETE, DROP, etc.
- Only SELECT and WITH queries are allowed
- Multiple statements (semicolon-separated) are rejected
- Logging records every query with duration and success status

**Why Chain of Thought?**

The LLM first produces a plan (which tables, which joins, which filters), then writes the SQL. This improves accuracy significantly.

**Why auto-retry?**

If the SQL fails (wrong column name, syntax error), the error is sent back to the LLM, which produces a corrected version. This makes the agent resilient.

### 5. Streamlit Dashboard (app.py)

Executives get a visual interface on top of the same database.

- KPI cards (revenue, net income, stores, countries)
- Bar charts (sales by brand)
- Line charts (revenue evolution)
- Pie chart (regional distribution)
- ABC analysis table

Uses **Plotly** for interactive charts, styled to match the CLI's visual identity.

---

## Data Flow

### Example: "Which brand is growing fastest?"

1. User types the question in the CLI
2. CLI passes it to the Data Agent
3. Agent asks the LLM to produce a plan
4. LLM returns: "join brands and sales_by_brand, filter latest year, order by growth"
5. Agent asks the LLM to write SQL using the plan and few-shot examples
6. LLM returns valid PostgreSQL
7. Agent validates the SQL (SELECT only, no forbidden keywords)
8. Agent executes the query on PostgreSQL
9. Result is a pandas DataFrame
10. Agent logs the query (question, SQL, success, duration)
11. Agent asks the LLM to explain the result in natural language
12. Agent asks the LLM to suggest 3 follow-up questions
13. CLI renders everything with Rich (plan panel, SQL panel, result table, answer, footer)

Total: ~150ms of LLM time + ~10ms of database time.

---

## Design Decisions

| Decision | Reasoning |
|---|---|
| PostgreSQL over SQLite | Production-grade, supports window functions well |
| Typer over argparse | Auto-help, type-safe, modern |
| Rich over plain print | Professional terminal output matters |
| Groq over OpenAI | Faster inference, free tier, Llama 3.3 quality |
| Llama 3.3 70B over smaller models | Better SQL generation accuracy |
| Streamlit over FastAPI+React | Faster to build, good enough for demos |
| SQLAlchemy over raw psycopg2 | Cleaner API, connection pooling |
| pandas over raw SQL results | Easier to work with, familiar to data teams |

---

## Extensibility

**Adding a new company (e.g. H&M):**

1. Create tables hm_brands, hm_sales_by_brand, hm_financials
2. Update the SCHEMA constant in agent.py
3. Add a --company flag to the CLI
4. Same agent works for both

**Adding a new report command:**

1. Add a function to cli.py with @app.command()
2. Use run_query to fetch data
3. Render with Rich tables

**Swapping the LLM:**

1. Change MODEL constant in agent.py
2. Same code works with any Groq-supported model

---

## Performance

- Average query latency: **~150 ms**
- Database query time: **~10 ms**
- Query log captures all timings

The bottleneck is the LLM (3 API calls per question: plan, SQL, explain).
Caching identical questions would reduce this further.

---

## Security

- API keys stored in .env (never committed)
- SQL injection impossible (LLM generates the SQL from a fixed schema)
- Forbidden keywords blocked at validation time
- Query log provides full audit trail

---

## What Would Change in Production

- Add authentication to the CLI
- Replace Groq with a private LLM endpoint
- Add connection pooling (SQLAlchemy already supports it)
- Add rate limiting per user
- Add Prometheus metrics
- Replace .env with a secrets manager (Vault, AWS Secrets Manager)
- Add CI/CD with GitHub Actions
- Add unit tests for the agent pipeline

---

Built with PostgreSQL 17, Python 3.11, Typer, Rich, Streamlit, Plotly, SQLAlchemy, and the Groq API.