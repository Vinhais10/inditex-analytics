# Inditex Analytics

**A complete business intelligence suite for Inditex - combining PostgreSQL, a professional CLI, an AI-powered Data Agent, and an interactive dashboard.**

**Real financial data (2023-2025) - Ask questions in plain English - AI writes the SQL - Full audit trail**

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Groq](https://img.shields.io/badge/Groq-GPT--OSS%20120B-F55036)](https://groq.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()

---

## Live Site

**[Open the live site](https://vinhais10.github.io/inditex-analytics/)** - explore the four interfaces of the project with direct links to the Data Agent and the Professional CLI.

---

## What This Is

Inditex is the world's largest fashion retailer - owner of **Zara, Bershka, Stradivarius, Massimo Dutti, Pull&Bear, and Oysho**.

This project is a complete **business intelligence suite** that answers real questions about Inditex's financial performance, combining **four interfaces** over the same PostgreSQL database:

| | Interface | What It Does |
|---|---|---|
| CLI | **Professional CLI** | Instant reports in your terminal (Typer + Rich) |
| AI | **Data Agent** | Ask questions in plain English - the AI writes the SQL |
| WEB | **Streamlit Dashboard** | Interactive charts and KPIs |
| DB | **PostgreSQL Database** | Real relational schema with joins, CTEs, window functions |

**Real business intelligence. Real data. Real engineering.**

---

## Features

### Data Agent (AI-Powered SQL)

- **Natural language to SQL** - English, Portuguese, or Spanish
- **Chain of Thought** - explains its reasoning *before* writing SQL
- **Few-shot prompting** - learns from curated examples for higher accuracy
- **Auto-retry** - if the SQL fails, the agent reads the error and fixes it
- **SQL validation** - only SELECT and WITH allowed (blocks all mutations)
- **Full audit trail** - every query logged to query_log table with timing
- **Follow-up suggestions** - the agent proposes 3 related questions
- **Three languages** - auto-detects English, Portuguese or Spanish and replies in the same language

### Professional CLI

- Built with **Typer** + **Rich** for a polished terminal experience
- Six commands: report, brands, abc, regions, growth, ask
- Colored tables, progress spinners, medals, ASCII bar charts
- Millisecond-level query timing displayed on every answer

### Dashboard

- 4 KPI cards (revenue, net income, stores, countries)
- Sales by brand (bar chart)
- Growth ranking (colored bars)
- Geographic distribution (donut chart)
- ABC portfolio analysis table

### Database

- **5 normalized tables** with proper foreign keys
- Window functions, CTEs, aggregations, and joins used throughout
- Query log for auditing and performance analysis
- Real Inditex financial data for 2023, 2024, and 2025

---

## How the Data Agent Works

The agent follows a **7-step pipeline**:

    "Which brand is growing fastest?"
                |
                v
    1. PLAN      LLM reasons about the approach
                |
                v
    2. GENERATE  LLM writes SQL (few-shot examples)
                |
                v
    3. VALIDATE  Block non-SELECT / non-WITH
                |
                v
    4. EXECUTE   Run on PostgreSQL (retry on error)
                |
                v
    5. LOG       Save to query_log with timing
                |
                v
    6. EXPLAIN   Natural language + business insight
                |
                v
    7. SUGGEST   3 follow-up questions

**The agent never invents data.** It builds SQL from a fixed schema, executes it against real data, and explains the result.

Read more in [ARCHITECTURE.md](ARCHITECTURE.md).

---

## Example Queries

Try asking the Data Agent anything from this list:

| Question | What It Answers |
|---|---|
| "Which brand is growing fastest?" | Top growth brand + rate |
| "What is the revenue per store?" | Operational efficiency |
| "How did revenue evolve from 2023 to 2025?" | YoY trend |
| "Which region accounts for more than 50% of sales?" | Geographic concentration |
| "Top 3 brands by growth with their market share" | Multi-metric analysis |
| "What is the profit margin in 2025?" | Profitability |

The agent works in **English, Portuguese, and Spanish** - it responds in the language of the question.

---

## Quick Start

### 1. Clone and install

    git clone https://github.com/Vinhais10/inditex-analytics.git
    cd inditex-analytics
    pip install -r requirements.txt

### 2. Set up PostgreSQL

Install PostgreSQL 17, then:

    psql -U postgres
    CREATE DATABASE inditex_db;

Load the schema and data (see queries.sql for the structure).

### 3. Configure environment

Copy .env.example to .env:

    DB_HOST=localhost
    DB_PORT=5432
    DB_NAME=inditex_db
    DB_USER=postgres
    DB_PASSWORD=your_password
    GROQ_API_KEY=your_groq_key

Get a free Groq API key at [console.groq.com/keys](https://console.groq.com/keys).

### 4. Run

**Data Agent (Streamlit):**

    py -m streamlit run agent_app.py

**Dashboard (Streamlit):**

    py -m streamlit run app.py

**CLI:**

    python cli.py --help
    python cli.py report
    python cli.py ask "Which brand is growing fastest?"

---

## Project Structure

    inditex-analytics/
    |-- agent.py                # Data Agent (AI SQL + Chain of Thought)
    |-- agent_app.py            # Streamlit app for the Data Agent
    |-- cli.py                  # Professional CLI (Typer + Rich)
    |-- app.py                  # Streamlit dashboard
    |-- db.py                   # Shared database interface
    |-- queries.sql             # All SQL queries, commented
    |-- insights.md             # Business analysis of the data
    |-- ARCHITECTURE.md         # Technical deep-dive
    |-- WHY.md                  # Problem statement and motivation
    |-- docs/                   # GitHub Pages site
    |-- requirements.txt
    |-- .env.example
    |-- .gitignore
    |-- README.md

---

## Business Insights

The project produced **six real findings** about Inditex - see [insights.md](insights.md):

| # | Insight |
|---|---|
| 1 | **Zara = 70.4% of sales** - high concentration risk |
| 2 | **Zara grows only 1% YoY** - the flagship is stagnating |
| 3 | **Oysho grows 15.5%** - small brands grow 15x faster |
| 4 | **Growth rate halved** from 7.47% (2024) to 3.19% (2025) |
| 5 | **Fewer stores, more revenue** - 232 fewer stores, +3.9B EUR revenue |
| 6 | **Zara + Bershka = 78.6%** - ABC Class A |

**Strategic takeaway:** Inditex is diversifying away from Zara while reducing physical stores - the classic "fewer, better" modern retail strategy.

---

## Tech Stack

| Layer | Tools |
|---|---|
| **Language** | Python 3.11 |
| **Database** | PostgreSQL 17 |
| **CLI** | Typer, Rich |
| **AI** | Groq API, GPT-OSS 120B |
| **Dashboard** | Streamlit, Plotly |
| **Data** | pandas, SQLAlchemy, psycopg2 |
| **Config** | python-dotenv |

---

## What This Project Demonstrates

- **PostgreSQL** - schema design, foreign keys, window functions, CTEs
- **Professional Python** - Typer, Rich, type hints, clean modules
- **AI Engineering** - Chain of Thought, few-shot prompting, SQL validation, auto-retry
- **LLM Integration** - Groq, prompt design, error recovery
- **Data Visualization** - Streamlit, Plotly
- **Software Architecture** - shared interfaces, separation of concerns
- **Business Analysis** - ABC analysis, growth ranking, executive summaries

---

## Roadmap

- [x] PostgreSQL schema with real Inditex data
- [x] Professional CLI with 6 commands
- [x] Data Agent with Chain of Thought
- [x] SQL validation and auto-retry
- [x] Query logging and audit trail
- [x] Streamlit dashboard
- [x] Business insights document
- [x] Technical architecture document
- [x] Three languages (EN / PT / ES)
- [x] Marketing site on GitHub Pages
- [ ] Add 2020-2022 historical data
- [ ] Support for multiple companies (H&M, Nike, Adidas)
- [ ] PDF report generation
- [ ] REST API (FastAPI)
- [ ] Unit tests for the agent pipeline

---

## License

MIT - see [LICENSE](LICENSE).

---

## Acknowledgements

- **Inditex** - for publishing detailed annual reports
- **Groq** - for fast inference on GPT-OSS
- **PostgreSQL community** - for the world's best open source database
- **Streamlit, Typer, Rich, Plotly** - for the frameworks

---

Built as part of a self-directed learning path applying real-world data analysis, SQL, and AI to business intelligence.
