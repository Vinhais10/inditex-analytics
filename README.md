# Inditex Analytics

**A complete business intelligence suite for Inditex â€” combining PostgreSQL, a professional CLI, an AI-powered Data Agent, and an interactive dashboard.**

**Real financial data (2023-2025) Â· Ask questions in plain English Â· AI writes the SQL Â· Full audit trail**

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Groq](https://img.shields.io/badge/Groq-Llama%203.3%2070B-F55036)](https://groq.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()

---

## ðŸ“Š See It in Action

![Dashboard](screenshots/dashboard.png)

> **Dashboard:** 4 KPI cards, sales by brand, growth ranking, and ABC portfolio analysis â€” all queried live from PostgreSQL.

![Data Agent](screenshots/agent.png)

> **Data Agent:** ask a question in plain English â€” the AI plans, writes the SQL, validates it, runs it, and explains the result with a business insight.

---

## ðŸŽ¯ What This Is

Inditex is the world's largest fashion retailer â€” owner of **Zara, Bershka, Stradivarius, Massimo Dutti, Pull&Bear, and Oysho**.

This project is a complete **business intelligence suite** that answers real questions about Inditex's financial performance, combining **four interfaces** over the same PostgreSQL database:

| | Interface | What It Does |
|---|---|---|
| ðŸ–¥ï¸ | **Professional CLI** | Instant reports in your terminal (Typer + Rich) |
| ðŸ¤– | **Data Agent** | Ask questions in plain English â€” the AI writes the SQL |
| ðŸ“Š | **Streamlit Dashboard** | Interactive charts and KPIs |
| ðŸ—„ï¸ | **PostgreSQL Database** | Real relational schema with joins, CTEs, window functions |

**Real business intelligence. Real data. Real engineering.**

---

## âœ¨ Features

### ðŸ¤– Data Agent (AI-Powered SQL)

- **Natural language to SQL** â€” English, Portuguese, or Spanish
- **Chain of Thought** â€” explains its reasoning *before* writing SQL
- **Few-shot prompting** â€” learns from curated examples for higher accuracy
- **Auto-retry** â€” if the SQL fails, the agent reads the error and fixes it
- **SQL validation** â€” only SELECT and WITH allowed (blocks all mutations)
- **Full audit trail** â€” every query logged to query_log table with timing
- **Follow-up suggestions** â€” the agent proposes 3 related questions

### ðŸ–¥ï¸ Professional CLI

- Built with **Typer** + **Rich** for a polished terminal experience
- Six commands: 
eport, rands, bc, 
egions, growth, sk
- Colored tables, progress spinners, medals, ASCII bar charts
- Millisecond-level query timing displayed on every answer

### ðŸ“Š Dashboard

- 4 KPI cards (revenue, net income, stores, countries)
- Sales by brand (bar chart)
- Growth ranking (colored bars)
- Geographic distribution (donut chart)
- ABC portfolio analysis table

### ðŸ—„ï¸ Database

- **5 normalized tables** with proper foreign keys
- Window functions, CTEs, aggregations, and joins used throughout
- Query log for auditing and performance analysis
- Real Inditex financial data for 2023, 2024, and 2025

---

## ðŸ§  How the Data Agent Works

The agent follows a **7-step pipeline**:

    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
    â”‚  "Which brand is growing fastest?"               â”‚
    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                          â–¼
    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
    â”‚  1. PLAN      LLM reasons about the approach     â”‚
    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                          â–¼
    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
    â”‚  2. GENERATE  LLM writes SQL (few-shot examples) â”‚
    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                          â–¼
    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
    â”‚  3. VALIDATE  Block non-SELECT / non-WITH        â”‚
    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                          â–¼
    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
    â”‚  4. EXECUTE   Run on PostgreSQL (retry on error) â”‚
    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                          â–¼
    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
    â”‚  5. LOG       Save to query_log with timing      â”‚
    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                          â–¼
    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
    â”‚  6. EXPLAIN   Natural language + business insightâ”‚
    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                          â–¼
    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
    â”‚  7. SUGGEST   3 follow-up questions              â”‚
    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

**The agent never invents data.** It builds SQL from a fixed schema, executes it against real data, and explains the result.

Read more in [ARCHITECTURE.md](ARCHITECTURE.md).

---

## ðŸ’¬ Example Queries

Try asking the Data Agent anything from this list:

| Question | What It Answers |
|---|---|
| "Which brand is growing fastest?" | Top growth brand + rate |
| "What is the revenue per store?" | Operational efficiency |
| "How did revenue evolve from 2023 to 2025?" | YoY trend |
| "Which region accounts for more than 50% of sales?" | Geographic concentration |
| "Top 3 brands by growth with their market share" | Multi-metric analysis |
| "What is the profit margin in 2025?" | Profitability |

The agent works in **English, Portuguese, and Spanish** â€” it responds in the language of the question.

---

## ðŸš€ Quick Start

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

**CLI:**
    python cli.py --help
    python cli.py report
    python cli.py ask "Which brand is growing fastest?"

**Dashboard:**
    streamlit run app.py

---

## ðŸ“ Project Structure

    inditex-analytics/
    â”œâ”€â”€ agent.py                # Data Agent (AI SQL + Chain of Thought)
    â”œâ”€â”€ cli.py                  # Professional CLI (Typer + Rich)
    â”œâ”€â”€ app.py                  # Streamlit dashboard
    â”œâ”€â”€ db.py                   # Shared database interface
    â”œâ”€â”€ queries.sql             # All SQL queries, commented
    â”œâ”€â”€ insights.md             # Business analysis of the data
    â”œâ”€â”€ ARCHITECTURE.md         # Technical deep-dive
    â”œâ”€â”€ WHY.md                  # Problem statement and motivation
    â”œâ”€â”€ screenshots/            # Product screenshots
    â”œâ”€â”€ requirements.txt
    â”œâ”€â”€ .env.example
    â”œâ”€â”€ .gitignore
    â””â”€â”€ README.md

---

## ðŸ“ˆ Business Insights

The project produced **six real findings** about Inditex â€” see [insights.md](insights.md):

| # | Insight |
|---|---|
| 1 | **Zara = 70.4% of sales** â€” high concentration risk |
| 2 | **Zara grows only 1% YoY** â€” the flagship is stagnating |
| 3 | **Oysho grows 15.5%** â€” small brands grow 15Ã— faster |
| 4 | **Growth rate halved** from 7.47% (2024) to 3.19% (2025) |
| 5 | **Fewer stores, more revenue** â€” 232 fewer stores, +â‚¬3.9B revenue |
| 6 | **Zara + Bershka = 78.6%** â€” ABC Class A |

**Strategic takeaway:** Inditex is diversifying away from Zara while reducing physical stores â€” the classic "fewer, better" modern retail strategy.

---

## ðŸ› ï¸ Tech Stack

| Layer | Tools |
|---|---|
| **Language** | Python 3.11 |
| **Database** | PostgreSQL 17 |
| **CLI** | Typer, Rich |
| **AI** | Groq API, Llama 3.3 70B |
| **Dashboard** | Streamlit, Plotly |
| **Data** | pandas, SQLAlchemy, psycopg2 |
| **Config** | python-dotenv |

---

## ðŸŽ“ What This Project Demonstrates

- **PostgreSQL** â€” schema design, foreign keys, window functions, CTEs
- **Professional Python** â€” Typer, Rich, type hints, clean modules
- **AI Engineering** â€” Chain of Thought, few-shot prompting, SQL validation, auto-retry
- **LLM Integration** â€” Groq, prompt design, error recovery
- **Data Visualization** â€” Streamlit, Plotly
- **Software Architecture** â€” shared interfaces, separation of concerns
- **Business Analysis** â€” ABC analysis, growth ranking, executive summaries

---

## ðŸ—ºï¸ Roadmap

- [x] PostgreSQL schema with real Inditex data
- [x] Professional CLI with 6 commands
- [x] Data Agent with Chain of Thought
- [x] SQL validation and auto-retry
- [x] Query logging and audit trail
- [x] Streamlit dashboard
- [x] Business insights document
- [x] Technical architecture document
- [ ] Add 2020-2022 historical data
- [ ] Support for multiple companies (H&M, Nike, Adidas)
- [ ] PDF report generation
- [ ] REST API (FastAPI)
- [ ] Web version of the agent
- [ ] Unit tests for the agent pipeline

---

## ðŸ“œ License

MIT â€” see [LICENSE](LICENSE).

---

## ðŸ™ Acknowledgements

- **Inditex** â€” for publishing detailed annual reports
- **Groq** â€” for fast inference on Llama 3.3
- **PostgreSQL community** â€” for the world's best open source database
- **Streamlit, Typer, Rich, Plotly** â€” for the frameworks

---

Built as part of a self-directed learning path applying real-world data analysis, SQL, and AI to business intelligence.
