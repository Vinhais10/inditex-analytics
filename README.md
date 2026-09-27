# Inditex Analytics

**Business intelligence suite for Inditex (Zara, Bershka, Massimo Dutti, and more) - built with PostgreSQL, a professional CLI, an AI-powered SQL agent, and an interactive dashboard.**

**Powered by real financial data (2023-2025) | Query the database in natural language | 100% open source**

![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-336791.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-dashboard-red.svg)
![Groq](https://img.shields.io/badge/AI-Groq-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## What This Is

A complete **business intelligence suite** that analyzes Inditex's financial data - the world's largest fashion retailer, owner of Zara, Bershka, Stradivarius, Massimo Dutti, Pull&Bear, and Oysho.

Unlike typical dashboards, this project combines **four interfaces** over the same PostgreSQL database:

| Interface | Purpose |
|---|---|
| **Professional CLI** | Fast reporting in your terminal (Typer + Rich) |
| **AI SQL Agent** | Ask questions in plain English or Portuguese - the AI writes the SQL |
| **Streamlit Dashboard** | Interactive charts and KPIs for executives |
| **PostgreSQL Database** | Real relational schema with joins, window functions, and CTEs |

**Real business intelligence, applied to a real company.**

---

## Features

### AI SQL Agent
- **Natural language to SQL** (English, Portuguese, or Spanish)
- **Chain of Thought** - explains its reasoning before writing SQL
- **Few-shot prompting** - learns from examples for higher accuracy
- **Auto-retry** - if the SQL fails, the agent fixes it automatically
- **SQL validation** - blocks non-SELECT queries (safety)
- **Query logging** - every query saved to query_log table
- **Follow-up suggestions** - suggests related questions to explore

### Professional CLI
- Built with **Typer + Rich** for a polished terminal experience
- Commands: report, brands, abc, regions, growth, ask
- Colored tables, progress spinners, medals, ASCII bar charts
- Duration tracking in milliseconds

### Dashboard (Streamlit)
- 4 KPI cards (revenue, net income, stores, countries)
- Sales by brand, growth rankings, region distribution
- ABC analysis for the brand portfolio

### PostgreSQL Database
- Normalized schema with foreign keys
- Real Inditex financial data (2023-2025)
- Window functions, CTEs, aggregations, joins
- Query log for auditing

---

## Quick Start

### 1. Clone and install

    git clone https://github.com/Vinhais10/inditex-analytics.git
    cd inditex-analytics
    pip install -r requirements.txt

### 2. Set up PostgreSQL

Install PostgreSQL 17 and create the database:

    CREATE DATABASE inditex_db;

### 3. Configure environment

Copy .env.example to .env and fill in:

    DB_HOST=localhost
    DB_PORT=5432
    DB_NAME=inditex_db
    DB_USER=postgres
    DB_PASSWORD=your_password
    GROQ_API_KEY=your_groq_api_key

Get a free Groq key at https://console.groq.com/keys

### 4. Run

CLI:

    python cli.py --help
    python cli.py report
    python cli.py ask "Which brand is growing fastest?"

Dashboard:

    streamlit run app.py

---

## How the AI Agent Works

The agent follows a 6-step pipeline:

1. PLAN - LLM thinks through the approach
2. GENERATE - LLM writes SQL using few-shot examples
3. VALIDATE - Block anything that is not SELECT/WITH
4. EXECUTE - Run query (retry once on failure)
5. LOG - Save to query_log table
6. EXPLAIN - Natural language answer + business insight
7. SUGGEST - 3 follow-up questions

**Why this matters:** the agent never invents data. It generates SQL from the schema, runs it, and explains real results.

---

## Project Structure

    inditex-analytics/
    |-- app.py                  # Streamlit dashboard
    |-- cli.py                  # Professional CLI (Typer + Rich)
    |-- agent.py                # AI SQL agent (Groq + Llama)
    |-- db.py                   # Database connection helper
    |-- requirements.txt
    |-- .env.example
    |-- .gitignore
    |-- README.md
    |-- insights.md             # Business insights from the data
    |-- queries.sql             # Commented SQL queries

---

## Business Insights

See insights.md for the full analysis. Key findings:

| # | Insight |
|---|---|
| 1 | Zara represents 70.4% of total sales - high concentration risk |
| 2 | Zara grows only 1% YoY - the flagship is stagnating |
| 3 | Oysho grows 15.5% - small brands grow 15x faster |
| 4 | Revenue growth slowed from 7.47% (2024) to 3.19% (2025) |
| 5 | Fewer stores, more revenue - 5,692 to 5,460 stores, revenue +3.9B |
| 6 | ABC analysis: Zara + Bershka = 78.6% of sales (Class A) |

**Strategic takeaway:** Inditex is diversifying away from Zara while reducing physical stores - a classic modern retail strategy.

---

## Tech Stack

| Layer | Tools |
|---|---|
| Language | Python 3.11 |
| Database | PostgreSQL 17 |
| CLI | Typer, Rich |
| AI | Groq API, Llama 3.3 70B |
| Dashboard | Streamlit, Plotly |
| Data | pandas, SQLAlchemy, psycopg2 |
| Config | python-dotenv |

---

## Roadmap

- [x] PostgreSQL schema with real Inditex data
- [x] Professional CLI with 6 commands
- [x] AI SQL agent with Chain of Thought
- [x] SQL validation and auto-retry
- [x] Query logging
- [x] Streamlit dashboard
- [ ] Add 2020-2022 historical data
- [ ] Support for multiple companies (H&M, Nike, Adidas)
- [ ] PDF report generation
- [ ] REST API (FastAPI)
- [ ] Web version of the agent

---

## License

MIT - see LICENSE.

---

Built as part of a self-directed learning path applying real-world data analysis, SQL, and AI to business intelligence.