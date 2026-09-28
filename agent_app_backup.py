"""Data Agent — Streamlit app with two-panel layout, memory, and multi-language support."""

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Data Agent — Inditex Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# GOOGLE FONTS
# ============================================================
st.markdown(
    """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;1,400&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    """,
    unsafe_allow_html=True,
)

# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown(
    """
    <style>
    .stApp { background-color: #050505; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }

    h1, h2, h3 {
        font-family: 'Playfair Display', Georgia, serif !important;
        letter-spacing: -0.02em;
        color: #ffffff;
    }
    p, div, span, label {
        font-family: 'Inter', system-ui, sans-serif;
    }

    .page-title {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 2.5rem;
        font-weight: 500;
        color: #ffffff;
        margin-bottom: 0.25rem;
        letter-spacing: -0.02em;
    }
    .page-title em { font-style: italic; color: #c9a961; }
    .page-sub {
        color: #9ca3af;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }

    .sidebar-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.2em;
        color: #c9a961;
        margin-bottom: 1rem;
    }

    .stButton > button {
        width: 100%;
        background: #0a0a0a !important;
        color: #cbd5e1 !important;
        border: 1px solid #1f1f1f !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
        text-align: left !important;
        font-size: 0.85rem !important;
        transition: all 0.2s !important;
        margin-bottom: 6px !important;
    }
    .stButton > button:hover {
        border-color: #c9a961 !important;
        color: #ffffff !important;
        background: rgba(201,169,97,0.05) !important;
    }

    .stChatMessage {
        background: #0a0a0a !important;
        border: 1px solid #1f1f1f !important;
        border-radius: 10px !important;
    }

    .stChatInput textarea {
        background: #0a0a0a !important;
        border: 1px solid #1f1f1f !important;
        color: #ffffff !important;
    }
    .stChatInput textarea:focus {
        border-color: #c9a961 !important;
        box-shadow: 0 0 0 1px #c9a961 !important;
    }

    .stCode, pre, code {
        background: #050505 !important;
        border: 1px solid #1f1f1f !important;
        color: #93c5fd !important;
        font-family: 'JetBrains Mono', monospace !important;
    }

    .streamlit-expanderHeader {
        background: #0a0a0a !important;
        color: #9ca3af !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.75rem !important;
    }

    hr { border-color: #1f1f1f !important; }

    .lang-badge {
        display: inline-block;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.65rem;
        padding: 2px 8px;
        border-radius: 4px;
        background: rgba(201,169,97,0.1);
        color: #c9a961;
        border: 1px solid rgba(201,169,97,0.3);
        letter-spacing: 0.1em;
        margin-bottom: 6px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# HEADER
# ============================================================
st.markdown(
    '<div class="page-title">Ask in English, Portuguese or Spanish. <em>Get SQL-backed answers.</em></div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="page-sub">The agent plans its approach, writes and validates the query, and returns a deterministic result.</div>',
    unsafe_allow_html=True,
)

st.divider()


# ============================================================
# LAYOUT: 2 PAINÉIS
# ============================================================
col_left, col_right = st.columns([1, 2.5], gap="large")


# ---------- Painel esquerdo ----------
with col_left:
    st.markdown('<div class="sidebar-title">Example questions</div>', unsafe_allow_html=True)

    examples = [
        ("🇬🇧 Which brand is growing fastest?", "en"),
        ("🇬🇧 How did revenue evolve from 2023 to 2025?", "en"),
        ("🇵🇹 Qual é a marca que cresce mais rápido?", "pt"),
        ("🇵🇹 Como evoluiu a receita entre 2023 e 2025?", "pt"),
        ("🇪🇸 ¿Qué marca está creciendo más rápido?", "es"),
        ("🇪🇸 ¿Cuál es el margen de beneficio en 2025?", "es"),
    ]

    for label, code in examples:
        if st.button(label, key=f"ex_{code}_{label}"):
            st.session_state.pending_question = label
            st.rerun()

    st.divider()

    if st.button("🗑️  Clear conversation", key="clear"):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.markdown(
        '<div style="font-size:0.7rem;color:#6b7280;line-height:1.8;">'
        '<div style="color:#c9a961;margin-bottom:4px;">MODEL</div>'
        'Groq · Llama 3.3 70B<br>'
        '<div style="color:#c9a961;margin-top:12px;margin-bottom:4px;">DATA</div>'
        'PostgreSQL · Inditex 2023–2025<br>'
        '<div style="color:#c9a961;margin-top:12px;margin-bottom:4px;">LANGUAGES</div>'
        'EN · PT · ES'
        '</div>',
        unsafe_allow_html=True,
    )


# ---------- Painel direito ----------
with col_right:
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Hi! Ask me anything about Inditex financial data — in **English**, **Portuguese** or **Spanish**. Try one of the examples on the left, or type your question below.",
            }
        ]

    # Render histórico
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            if msg.get("language"):
                st.markdown(
                    f'<span class="lang-badge">{msg["language"].upper()}</span>',
                    unsafe_allow_html=True,
                )
            st.markdown(msg["content"])

            if msg.get("sql"):
                with st.expander("🔍 View generated SQL"):
                    st.code(msg["sql"], language="sql")
                    st.download_button(
                        "⬇️ Download SQL",
                        data=msg["sql"],
                        file_name="query.sql",
                        mime="text/plain",
                        key=f"dl_{id(msg)}",
                    )

            if msg.get("data_preview"):
                with st.expander("📊 View raw result"):
                    st.dataframe(msg["data_preview"], use_container_width=True)

            if msg.get("duration_ms"):
                st.caption(f"⚡ Executed in {msg['duration_ms']} ms")

            if msg.get("followups"):
                st.markdown("**You may also ask:**")
                for fu in msg["followups"]:
                    st.markdown(f"- {fu}")

    # Input
    user_input = st.chat_input("Ask a question about the Inditex data...")

    if st.session_state.get("pending_question"):
        user_input = st.session_state.pending_question
        st.session_state.pending_question = None

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    from agent import ask as agent_ask

                    # --- Memória: últimas 6 mensagens (3 pares) ---
                    history = [
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages[-7:-1]
                        if m.get("content")
                    ]

                    try:
                        response = agent_ask(user_input, verbose=False, history=history)
                    except TypeError:
                        # Fallback se o agent.py ainda não tiver o parâmetro history
                        response = agent_ask(user_input, verbose=False)

                    if "error" in response:
                        answer = f"❌ {response['error']}"
                        st.error(answer)
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": answer,
                            "language": response.get("language"),
                        })
                    else:
                        lang = response.get("language", "en")
                        st.markdown(
                            f'<span class="lang-badge">{lang.upper()}</span>',
                            unsafe_allow_html=True,
                        )

                        answer = response["explanation"]
                        st.markdown(answer)

                        sql = response.get("sql")
                        if sql:
                            with st.expander("🔍 View generated SQL"):
                                st.code(sql, language="sql")
                                st.download_button(
                                    "⬇️ Download SQL",
                                    data=sql,
                                    file_name="query.sql",
                                    mime="text/plain",
                                    key=f"dl_new_{hash(sql)}",
                                )

                        result_df = response.get("result")
                        data_preview = None
                        if result_df is not None and not result_df.empty:
                            data_preview = result_df.head(50)
                            with st.expander("📊 View raw result"):
                                st.dataframe(data_preview, use_container_width=True)

                        duration = response.get("duration_ms")
                        if duration:
                            st.caption(f"⚡ Executed in {duration} ms")

                        followups = response.get("followups")
                        if followups:
                            st.markdown("**You may also ask:**")
                            for fu in followups:
                                st.markdown(f"- {fu}")

                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": answer,
                            "sql": sql,
                            "duration_ms": duration,
                            "followups": followups,
                            "data_preview": data_preview,
                            "language": lang,
                        })
                except Exception as e:
                    answer = f"❌ Error: {e}"
                    st.error(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
