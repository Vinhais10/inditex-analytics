"""Inditex Analytics - Streamlit Dashboard."""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from db import run_query

st.set_page_config(
    page_title="Inditex Analytics",
    layout="wide",
    initial_sidebar_state="collapsed",
)

COLORS = {
    "primary": "#8B1A1A",
    "success": "#10B981",
    "danger":  "#EF4444",
    "warning": "#D4AF37",
    "text":    "#F1F5F9",
    "muted":   "#94A3B8",
}

st.markdown(
    """
    <style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    h1, h2, h3 { letter-spacing: -0.02em; font-family: 'Playfair Display', Georgia, serif; }
    .kpi-card {
        background: #0A0E1A;
        border: 1px solid #1F2637;
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


@st.cache_data(ttl=300)
def get_results():
    return run_query("""
        SELECT b.brand_name, s.sales_millions, s.growth_pct
        FROM sales_by_brand s
        JOIN brands b ON s.brand_id = b.brand_id
        ORDER BY s.sales_millions DESC;
    """)


@st.cache_data(ttl=300)
def get_financials():
    return run_query("SELECT * FROM financials ORDER BY year;")


@st.cache_data(ttl=300)
def get_regions():
    return run_query("SELECT * FROM sales_by_region ORDER BY sales_pct DESC;")


result = get_results()
financials = get_financials()
regions = get_regions()

latest = financials.iloc[-1]
prev = financials.iloc[-2]

revenue = latest["revenue_millions"]
net_income = latest["net_income_millions"]
stores = latest["stores_count"]
countries = latest["countries_count"]


# ============================================================
# HEADER
# ============================================================
st.title("Inditex Analytics")
st.caption("Business intelligence for the world's largest fashion retailer — live data from PostgreSQL.")
st.divider()


# ============================================================
# KPI CARDS
# ============================================================
k1, k2, k3, k4 = st.columns(4)

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
            <div class="kpi-value">{stores:,.0f}</div>
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
            <div class="kpi-value" style="color:#D4AF37;">{countries:,.0f}</div>
            <div class="kpi-sub">Global presence</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()


# ============================================================
# CHART 1 — Sales by brand
# ============================================================
st.subheader("Sales by Brand (2025)")

fig1 = go.Figure()
fig1.add_trace(go.Bar(
    x=result["brand_name"],
    y=result["sales_millions"],
    marker_color=COLORS["primary"],
    text=[f"€{v:,.0f}M" for v in result["sales_millions"]],
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
    yaxis=dict(title="Sales (millions €)", gridcolor="#1F2637"),
    showlegend=False,
)
st.plotly_chart(fig1, use_container_width=True)


# ============================================================
# CHART 2 — Growth by brand
# ============================================================
st.subheader("Growth by Brand (YoY %)")

growth_sorted = result.sort_values("growth_pct", ascending=True)
colors = [
    COLORS["success"] if v >= 10 else COLORS["warning"] if v >= 3 else COLORS["danger"]
    for v in growth_sorted["growth_pct"]
]

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
    xaxis=dict(title="Growth %", gridcolor="#1F2637"),
    yaxis=dict(tickfont=dict(size=14)),
    showlegend=False,
)
st.plotly_chart(fig2, use_container_width=True)


# ============================================================
# CHART 3 + ABC
# ============================================================
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Sales by Region")
    fig3 = go.Figure(go.Pie(
        labels=regions["region"],
        values=regions["sales_pct"],
        hole=0.5,
        marker=dict(colors=[COLORS["primary"], COLORS["success"], COLORS["warning"], COLORS["danger"]]),
        textinfo="label+percent",
        textfont=dict(color=COLORS["text"], size=13),
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
    st.subheader("ABC Analysis")
    abc = result.copy()
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
st.subheader("Financials (2023–2025)")

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
    xaxis=dict(title="Year", gridcolor="#1F2637", tickmode="linear"),
    yaxis=dict(title="€ Millions", gridcolor="#1F2637"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    hovermode="x unified",
)
st.plotly_chart(fig4, use_container_width=True)


# ============================================================
# FOOTER
# ============================================================
st.divider()
st.caption("Built with PostgreSQL · Streamlit · Groq Llama 3.3 · Data: Inditex annual reports 2023–2025")