"""Professional CLI — Streamlit reference app."""

import streamlit as st

st.set_page_config(
    page_title="Professional CLI — Inditex Analytics",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# DESIGN SYSTEM
# ============================================================
st.markdown(
    """
    <style>
    .stApp { background-color: #050505; }
    .block-container { padding-top: 3rem; padding-bottom: 3rem; max-width: 1100px; }
    h1, h2, h3 { font-family: 'Inter', sans-serif; letter-spacing: -0.02em; color: #ffffff; }
    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.5rem;
        letter-spacing: -0.03em;
    }
    .hero-title em { font-style: italic; color: #c9a961; }
    .hero-sub { color: #9ca3af; font-size: 1.05rem; margin-bottom: 2.5rem; }
    .cmd-card {
        background: #0a0a0a;
        border: 1px solid #1f1f1f;
        border-radius: 10px;
        padding: 24px 28px;
        margin-bottom: 20px;
        transition: all 0.3s;
    }
    .cmd-card:hover {
        border-color: #c9a961;
        background: rgba(201, 169, 97, 0.03);
    }
    .cmd-name {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1rem;
        color: #c9a961;
        margin-bottom: 8px;
        font-weight: 500;
    }
    .cmd-desc {
        color: #9ca3af;
        font-size: 0.9rem;
        margin-bottom: 16px;
    }
    .output-block {
        background: #050505;
        border: 1px solid #1f1f1f;
        border-radius: 6px;
        padding: 16px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        color: #d1d5db;
        overflow-x: auto;
        white-space: pre;
        line-height: 1.6;
    }
    .output-block .gold { color: #c9a961; }
    .output-block .green { color: #4ade80; }
    .output-block .red { color: #f87171; }
    .output-block .dim { color: #6b7280; }
    .output-block .blue { color: #93c5fd; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# HEADER
# ============================================================
st.markdown(
    '<div class="hero-title">The <em>command line</em>, done right.</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="hero-sub">Six commands with colored tables, medals, and progress spinners. Built with Typer and Rich. Below is a reference of what each command does and what its output looks like.</div>',
    unsafe_allow_html=True,
)

st.divider()

# ============================================================
# COMMANDS
# ============================================================

# 1. report
st.markdown(
    """
    <div class="cmd-card">
        <div class="cmd-name">$ python cli.py report [--year 2025]</div>
        <div class="cmd-desc">Show a financial report for a given year (default: 2025).</div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.code(
    """╭─────────────────────────────────────────────────────╮
│   INDITEX ANALYTICS  ·  Business Intelligence CLI   │
╰─────────────────────────────────────────────────────╯

Financial Report — 2025

┌───────────────────┬────────────┐
│  Revenue          │  €39,864M  │
│  Net Income       │   €6,220M  │
│  Gross Margin     │    58.30%  │
│  Stores           │   5,460.0  │
│  Countries        │      97.0  │
└───────────────────┴────────────┘

YoY revenue growth: +3.19%""",
    language="text",
)

# 2. brands
st.markdown(
    """
    <div class="cmd-card">
        <div class="cmd-name">$ python cli.py brands</div>
        <div class="cmd-desc">Sales and growth by brand, ordered by sales.</div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.code(
    """Brand           Sales (€M)         Growth
─────────────── ─────────────────  ──────
Zara            €28,051M  (70.4%)   +1.0%
Bershka         €3,286M   (8.2%)    +12.2%
Stradivarius    €3,002M   (7.5%)    +12.7%
Pull&Bear       €2,546M   (6.4%)    +3.1%
Massimo Dutti   €2,019M   (5.1%)    +3.0%
Oysho           €960M     (2.4%)    +15.5%

Total: €39,864M""",
    language="text",
)

# 3. abc
st.markdown(
    """
    <div class="cmd-card">
        <div class="cmd-name">$ python cli.py abc</div>
        <div class="cmd-desc">ABC portfolio analysis (Class A/B/C classification).</div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.code(
    """Class  Brand            Sales (€M)  Cumulative %
─────  ───────────────  ──────────  ────────────
  A    Zara              €28,051M       70.37%
  A    Bershka           €3,286M        78.61%
  B    Stradivarius      €3,002M        86.14%
  B    Pull&Bear         €2,546M        92.53%
  C    Massimo Dutti     €2,019M        97.59%
  C    Oysho             €960M         100.00%

Legend:
  A = Top 80% of sales (core portfolio)
  B = 80-95% (secondary)
  C = 95-100% (long tail)""",
    language="text",
)

# 4. regions
st.markdown(
    """
    <div class="cmd-card">
        <div class="cmd-name">$ python cli.py regions</div>
        <div class="cmd-desc">Sales distribution by geographic region.</div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.code(
    """Region                Share
────────────────────  ──────────────────────────────
Europe (excl. Spain)  █████████████████████████ 51.30%
Americas              ████████ 17.80%
Spain                 ███████ 15.90%
Asia & Rest of World  ███████ 15.00%""",
    language="text",
)

# 5. growth
st.markdown(
    """
    <div class="cmd-card">
        <div class="cmd-name">$ python cli.py growth</div>
        <div class="cmd-desc">Growth ranking of all brands.</div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.code(
    """#  Brand           Growth   Size (€M)
─  ──────────────  ───────  ──────────
1  Oysho           +15.50%      €960M
2  Stradivarius    +12.70%    €3,002M
3  Bershka         +12.20%    €3,286M
4  Pull&Bear        +3.10%    €2,546M
5  Massimo Dutti    +3.00%    €2,019M
6  Zara             +1.00%   €28,051M""",
    language="text",
)

# 6. ask
st.markdown(
    """
    <div class="cmd-card">
        <div class="cmd-name">$ python cli.py ask "Which brand is growing fastest?"</div>
        <div class="cmd-desc">Natural language query via the AI Data Agent.</div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.code(
    """Agent Plan
- Use sales_by_brand joined to brands
- Filter to the most recent year
- Order by growth_pct descending

Generated SQL
SELECT b.brand_name, s.growth_pct
FROM sales_by_brand s
JOIN brands b ON b.brand_id = s.brand_id
ORDER BY s.growth_pct DESC LIMIT 1;

Result
brand_name  growth_pct
──────────  ──────────
Oysho            15.5

Answer
The fastest-growing brand is Oysho, with a growth rate of 15.5%.

Executed in 146 ms""",
    language="text",
)

st.divider()

# ============================================================
# FOOTER
# ============================================================
st.markdown(
    """
    <div style="text-align:center; color:#6b7280; font-size:0.8rem; padding: 2rem 0;">
        Built with <span style="color:#c9a961;">Typer</span> ·
        <span style="color:#c9a961;">Rich</span> ·
        <span style="color:#c9a961;">PostgreSQL</span> ·
        <span style="color:#c9a961;">Groq Llama 3.3</span>
    </div>
    """,
    unsafe_allow_html=True,
)
