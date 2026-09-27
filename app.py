"""Inditex Analytics Dashboard - Streamlit app."""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from db import run_query

st.set_page_config(
    page_title="Inditex Analytics",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

COLORS = {
    "primary": "#6366F1",
    "success": "#10B981",
    "danger":  "#EF4444",
    "warning": "#F59E0B",
    "text":    "#F1F5F9",
    "muted":   "#94A3B8",
}

st.markdown(
    """
    <style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    h1, h2, h3 { letter-spacing: -0.02em; }
    .kpi-card {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
        height: 100%;
    }
    .kpi-label {
        color: #94A3B8;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 8px;
    }
    .kpi-value {
        color: #F1F5F9;
        font-size: 1.8rem;
        font-weight: 700;
        line-height: 1.1;
    }
    .kpi-sub {
        color: #94A3B8;
        font-size: 0.8rem;
        margin-top: 6px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🛍️ Inditex Analytics")
st.caption("Business intelligence dashboard built with PostgreSQL + Streamlit — using real Inditex data (2023-2025).")


# ============================================================
# LOAD DATA
# ============================================================
@st.cache_data(ttl=3600)
def load_data():
    financials = run_query("SELECT * FROM financials ORDER BY year;")
    by_brand   = run_query("""
        SELECT b.brand_name, s.sales_millions, s.growth_pct
        FROM sales_by_brand s
        JOIN brands b ON s.brand_id = b.brand_id
        ORDER BY s.sales_millions DESC;
    """)
    by_region  = run_query("SELECT * FROM sales_by_region ORDER BY sales_pct DESC;")
    return financials, by_brand, by_region


financials, by_brand, by_region = load_data()

latest = financials.iloc[-1]
prev = financials.iloc[-2]


# ============================================================
# KPI CARDS
# ============================================================
k1, k2, k3, k4 = st.columns(4)

revenue = latest["revenue_millions"]
net_income = latest["net_income_millions"]
stores = latest["stores_count"]
countries = latest["countries_count"]

with k1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Revenue (2025)</div>
            <div class="kpi-value">€{revenue:,.0f}M</div>
            <div class="kpi-sub">+{((revenue - prev['revenue_millions']) / prev['revenue_millions'] * 100):.2f}% YoY</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with k2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Net Income</div>
            <div class="kpi-value" style="color:#10B981;">€{net_income:,.0f}M</div>
            <div class="kpi-sub">Margin: {net_income / revenue * 100:.1f}%</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with k3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Stores</div>
            <div class="kpi-value">{stores:,}</div>
            <div class="kpi-sub">Worldwide</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with k4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Countries</div>
            <div class="kpi-value" style="color:#F59E0B;">{countries}</div>
            <div class="kpi-sub">Global presence</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()


# ============================================================
# CHART 1 — Sales by brand
# ============================================================
st.subheader("💰 Sales by Brand (2025)")

fig1 = go.Figure()
fig1.add_trace(go.Bar(
    x=by_brand["brand_name"],
    y=by_brand["sales_millions"],
    marker_color=COLORS["primary"],
    text=[f"€{v:,.0f}M" for v in by_brand["sales_millions"]],
    textposition="outside",
    textfont=dict(size=13, color=COLORS["text"]),
    hovertemplate="<b>%{x}</b><br>€%{y:,.0f}M<extra></extra>",
))
fig1.update_layout(
    height=400,
    margin=dict(l=10, r=10, t=40, b=10),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=COLORS["text"], size=13),
    xaxis=dict(title="Brand", tickfont=dict(size=14)),
    yaxis=dict(title="Sales (millions €)", gridcolor="#334155"),
    showlegend=False,
)
st.plotly_chart(fig1, use_container_width=True)


# ============================================================
# CHART 2 — Growth by brand
# ============================================================
st.subheader("📈 Growth by Brand (YoY %)")

growth_sorted = by_brand.sort_values("growth_pct", ascending=True)
colors = [COLORS["success"] if v >= 10 else COLORS["warning"] if v >= 3 else COLORS["danger"]
          for v in growth_sorted["growth_pct"]]

fig2 = go.Figure()
fig2.add_trace(go.Bar(
    x=growth_sorted["growth_pct"],
    y=growth_sorted["brand_name"],
    orientation="h",
    marker_color=colors,
    text=[f"+{v:.1f}%" for v in growth_sorted["growth_pct"]],
    textposition="outside",
    textfont=dict(size=13, color=COLORS["text"]),
    hovertemplate="<b>%{y}</b><br>%{x:.2f}%<extra></extra>",
))
fig2.update_layout(
    height=350,
    margin=dict(l=10, r=10, t=40, b=10),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=COLORS["text"], size=13),
    xaxis=dict(title="Growth %", gridcolor="#334155"),
    yaxis=dict(tickfont=dict(size=14)),
    showlegend=False,
)
st.plotly_chart(fig2, use_container_width=True)


# ============================================================
# CHART 3 — Sales by region (pie)
# ============================================================
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("🌍 Sales by Region")
    fig3 = go.Figure(go.Pie(
        labels=by_region["region"],
        values=by_region["sales_pct"],
        hole=0.5,
        marker=dict(colors=[COLORS["primary"], COLORS["success"], COLORS["warning"], COLORS["danger"]]),
        textinfo="label+percent",
        textfont=dict(color=COLORS["text"], size=13),
        hovertemplate="<b>%{label}</b><br>%{value:.2f}%<extra></extra>",
    ))
    fig3.update_layout(
        height=400,
        margin=dict(l=10, r=10, t=40, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=COLORS["text"], size=13),
        showlegend=False,
    )
    st.plotly_chart(fig3, use_container_width=True)

with col_b:
    st.subheader("📊 ABC Analysis")
    abc = by_brand.copy()
    abc["cumulative_pct"] = abc["sales_millions"].cumsum() / abc["sales_millions"].sum() * 100
    abc["class"] = abc["cumulative_pct"].apply(
        lambda x: "A" if x <= 80 else "B" if x <= 95 else "C"
    )
    st.dataframe(
        abc[["brand_name", "sales_millions", "cumulative_pct", "class"]].rename(columns={
            "brand_name": "Brand",
            "sales_millions": "Sales (€M)",
            "cumulative_pct": "Cumulative %",
            "class": "Class",
        }),
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# CHART 4 — Financials over time
# ============================================================
st.subheader("📅 Financials (2023-2025)")

fig4 = go.Figure()
fig4.add_trace(go.Scatter(
    x=financials["year"], y=financials["revenue_millions"],
    mode="lines+markers+text",
    name="Revenue (€M)",
    line=dict(color=COLORS["primary"], width=3),
    marker=dict(size=12),
    text=[f"€{v:,.0f}M" for v in financials["revenue_millions"]],
    textposition="top center",
    textfont=dict(size=12, color=COLORS["text"]),
))
fig4.add_trace(go.Scatter(
    x=financials["year"], y=financials["net_income_millions"],
    mode="lines+markers+text",
    name="Net Income (€M)",
    line=dict(color=COLORS["success"], width=3),
    marker=dict(size=12),
    text=[f"€{v:,.0f}M" for v in financials["net_income_millions"]],
    textposition="bottom center",
    textfont=dict(size=12, color=COLORS["text"]),
))
fig4.update_layout(
    height=400,
    margin=dict(l=10, r=10, t=40, b=10),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=COLORS["text"], size=13),
    xaxis=dict(title="Year", gridcolor="#334155", tickmode="linear"),
    yaxis=dict(title="€ Millions", gridcolor="#334155"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    hovermode="x unified",
)
st.plotly_chart(fig4, use_container_width=True)


# ============================================================
# FOOTER
# ============================================================
st.divider()
st.caption("Built with PostgreSQL + Streamlit · Data source: Inditex annual reports 2023-2025")
