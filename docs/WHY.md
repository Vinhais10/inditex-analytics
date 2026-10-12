# Why This Project

## The Problem

Retail businesses generate enormous amounts of financial data every quarter. Managers, analysts, and executives need to answer questions like:

- Which brand is growing fastest?
- Are we becoming more efficient per store?
- Where is our revenue concentrated?

Traditionally, getting these answers requires:
1. Writing SQL manually (slow, error-prone)
2. Building dashboards for every question (rigid, not scalable)
3. Waiting for a data team (bottleneck)

## The Solution

**Inditex Analytics** demonstrates a modern alternative: a business intelligence suite that:

- Stores financial data in a **proper relational database** (PostgreSQL)
- Provides a **professional CLI** for instant reports
- Lets anyone ask questions in **plain English or Portuguese**
- Uses an **AI SQL Agent** that generates and runs the SQL automatically
- Explains results with **business insight**, not just raw numbers

## Why Inditex?

Inditex is the world's largest fashion retailer, owner of Zara, Bershka, Stradivarius, Massimo Dutti, Pull&Bear, and Oysho. It publishes detailed annual reports, making it a perfect real-world case study.

The data is **real** — 2023, 2024, and 2025 financials.

## What Makes This Different

Most portfolio projects are:
- Dashboards with static CSV data
- Notebooks that end with a chart
- AI demos that call an API and return text

This project combines:
- **A real database schema** (not CSVs)
- **A professional CLI** (Typer + Rich)
- **A real AI agent** with Chain of Thought, auto-retry, and validation
- **A dashboard** as an additional interface
- **Business analysis** that any stakeholder can understand

It is not a demo. It is a **system**.

## Who Is This For

- **Analysts** who want to query data without writing SQL
- **Managers** who need quick answers
- **Engineers** who want to see how a text-to-SQL agent is built
- **Recruiters** looking for evidence of real, production-grade work

---

Built with PostgreSQL, Python, and the Groq API (Llama 3.3 70B).