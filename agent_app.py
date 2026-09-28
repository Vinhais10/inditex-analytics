"""Data Agent — Streamlit app. Final stable."""

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

WELCOME_MSG = {
    "role": "assistant",
    "content": "Hi! I can answer questions about Inditex financial data from **2023 to 2025** only. What would you like to know?",
}

st.set_page_config(
    page_title="Data Agent — Inditex Analytics",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;1,400&family=Lora:ital,wght@0,400;0,500;1,400&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <style>
    .stApp { background-color: #050505; }

    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
        max-width: 100% !important;
        width: 100% !important;
    }
    [data-testid="stAppViewContainer"] > .main {
        margin-left: 0 !important;
        padding-left: 0 !important;
    }
    [data-testid="stAppViewBlockContainer"],
    .main .block-container,
    section.main > div {
        margin-left: 0 !important;
        max-width: 100% !important;
        padding-left: 1rem !important;
    }
    [data-testid="column"] { padding-left: 0.5rem !important; }

    #MainMenu { visibility: hidden; }
    header { visibility: hidden; }
    footer { visibility: hidden; }

    h1, h2, h3 {
        font-family: 'Playfair Display', Georgia, serif !important;
        letter-spacing: -0.02em;
        color: #ffffff;
    }
    p, div, span, label { font-family: 'Inter', system-ui, sans-serif; }

    .page-title {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 3.4rem;
        font-weight: 500;
        color: #ffffff;
        margin-bottom: 0;
        letter-spacing: -0.02em;
        line-height: 1.05;
    }
    .page-title em { font-style: italic; color: #c9a961; }

    .page-sub {
        color: #6b7280;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        margin-top: 1.1rem;
        margin-bottom: 1rem;
    }
    .page-sub span { color: #c9a961; }

    .stChatMessage p, .stChatMessage li {
        font-family: 'Lora', Georgia, serif !important;
        font-size: 1.02rem !important;
        line-height: 1.75 !important;
        letter-spacing: 0.005em !important;
        color: #e5e7eb;
    }
    .stChatMessage strong, .stChatMessage b {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    .stChatMessage em, .stChatMessage i { color: #c9a961 !important; }

    .stChatMessage {
        background: #0a0a0a !important;
        border: 1px solid #1f1f1f !important;
        border-radius: 10px !important;
        padding: 18px 22px !important;
    }
    .stChatMessage > div:first-child:has([data-testid^="chatAvatarIcon"]) {
        display: none !important;
    }
    .stChatMessage > div:first-child > div:first-child > div:first-child > div:first-child > span {
        display: none !important;
    }

    .stChatMessage [data-testid="stExpander"] {
        border: 1px solid #1f1f1f !important;
        border-radius: 8px !important;
        background: #050505 !important;
        margin-top: 6px !important;
        overflow: hidden !important;
    }
    .stChatMessage [data-testid="stExpander"] summary,
    .stChatMessage .streamlit-expanderHeader {
        background: #0a0a0a !important;
        color: #9ca3af !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.72rem !important;
        padding: 8px 12px !important;
        list-style: none !important;
        display: flex !important;
        align-items: center !important;
    }
    .stChatMessage [data-testid="stExpander"] summary::before,
    .stChatMessage [data-testid="stExpander"] summary::after,
    .stChatMessage [data-testid="stExpander"] summary::marker {
        content: none !important;
        display: none !important;
    }
    .stChatMessage [data-testid="stExpander"] summary svg {
        width: 14px !important;
        height: 14px !important;
        margin-right: 8px !important;
        color: #c9a961 !important;
        flex-shrink: 0 !important;
    }
    .stChatMessage [data-testid="stExpander"] details > div {
        background: #050505 !important;
        padding: 12px 16px !important;
        border-top: 1px solid #1f1f1f !important;
    }

    .info-box {
        background: #0a0a0a;
        border: 1px solid #1f1f1f;
        border-radius: 10px;
        padding: 14px 16px;
        font-size: 0.8rem;
        color: #9ca3af;
        line-height: 1.8;
    }
    .info-box .label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.62rem;
        color: #c9a961;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        display: block;
        margin-bottom: 6px;
    }

    .stButton > button {
        width: 100%;
        background: #0a0a0a !important;
        color: #cbd5e1 !important;
        border: 1px solid #1f1f1f !important;
        border-radius: 8px !important;
        padding: 8px 14px !important;
        text-align: left !important;
        font-size: 0.8rem !important;
        transition: all 0.2s !important;
    }
    .stButton > button:hover {
        border-color: #c9a961 !important;
        color: #ffffff !important;
        background: rgba(201,169,97,0.05) !important;
    }

    [data-testid="stChatInput"] {
        background: #0a0a0a !important;
        border: 1px solid #c9a961 !important;
        border-radius: 10px !important;
    }
    [data-testid="stChatInput"] textarea {
        background: #0a0a0a !important;
        border: none !important;
        color: #ffffff !important;
        font-size: 0.9rem !important;
        font-family: 'Inter', system-ui, sans-serif !important;
        box-shadow: none !important;
    }
    [data-testid="stChatInput"] textarea:focus {
        outline: none !important;
        box-shadow: none !important;
    }
    [data-testid="stChatInput"] textarea::placeholder {
        color: #6b7280 !important;
    }

    .stCode, pre, code {
        background: #050505 !important;
        border: 1px solid #1f1f1f !important;
        color: #93c5fd !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.78rem !important;
    }

    hr { border-color: #1f1f1f !important; margin: 0.75rem 0 !important; }

    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #1f1f1f; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #2f2f2f; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="page-title">Ask <em>the agent</em></div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="page-sub">Inditex Analytics · <span>English</span> · <span>Portugues</span> · <span>Espanol</span></div>',
    unsafe_allow_html=True,
)
st.divider()


col_left, col_right = st.columns([1, 2.2], gap="large")


with col_left:
    st.markdown(
        '<div class="info-box">'
        '<span class="label">How to use</span>'
        'Type a question about Inditex financial data in the chat on the right.<br><br>'
        'The agent will:<br>'
        '&nbsp;&nbsp;1. Plan the approach<br>'
        '&nbsp;&nbsp;2. Write the SQL<br>'
        '&nbsp;&nbsp;3. Validate it (SELECT only)<br>'
        '&nbsp;&nbsp;4. Run it on PostgreSQL<br>'
        '&nbsp;&nbsp;5. Explain the result<br>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    st.markdown(
        '<div class="info-box">'
        '<span class="label">Ask about</span>'
        'Sales by brand · Regional breakdown · Growth rates · Profit margins · Store count · Revenue evolution · Market concentration'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    if st.button("Clear conversation", key="clear"):
        st.session_state.messages = [dict(WELCOME_MSG)]
        st.rerun()

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    st.markdown(
        '<div style="font-size:0.68rem;color:#6b7280;line-height:1.8;">'
        '<div style="color:#c9a961;margin-bottom:4px;letter-spacing:0.2em;">MODEL</div>'
        'Groq · GPT-OSS 120B<br>'
        '<div style="color:#c9a961;margin-top:10px;margin-bottom:4px;letter-spacing:0.2em;">DATABASE</div>'
        'PostgreSQL · Inditex'
        '</div>',
        unsafe_allow_html=True,
    )


with col_right:
    if "messages" not in st.session_state or not st.session_state.messages:
        st.session_state.messages = [dict(WELCOME_MSG)]

    chat_box = st.container(height=420)

    with chat_box:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                if msg.get("sql"):
                    with st.expander("View generated SQL"):
                        st.code(msg["sql"], language="sql")
                if msg.get("data_preview") is not None:
                    with st.expander("View raw result"):
                        st.dataframe(msg["data_preview"], use_container_width=True)
                if msg.get("duration_ms"):
                    st.caption(f"Executed in {msg['duration_ms']} ms")

    user_input = st.chat_input("Ask a question about the Inditex data...")

    if st.session_state.get("pending_question"):
        user_input = st.session_state.pending_question
        st.session_state.pending_question = None

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with chat_box:
            with st.chat_message("user"):
                st.markdown(user_input)

        with chat_box:
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        from agent import ask as agent_ask
                        history = [
                            {"role": m["role"], "content": m["content"]}
                            for m in st.session_state.messages[-7:-1]
                            if m.get("content")
                        ]
                        try:
                            response = agent_ask(user_input, verbose=False, history=history)
                        except TypeError:
                            response = agent_ask(user_input, verbose=False)

                        if "error" in response:
                            answer = f"Error: {response['error']}"
                            st.error(answer)
                            st.session_state.messages.append({"role": "assistant", "content": answer})
                        else:
                            answer = response["explanation"]
                            st.markdown(answer)

                            sql = response.get("sql")
                            if sql:
                                with st.expander("View generated SQL"):
                                    st.code(sql, language="sql")

                            result_df = response.get("result")
                            data_preview = None
                            if result_df is not None and not result_df.empty:
                                data_preview = result_df.head(50)
                                with st.expander("View raw result"):
                                    st.dataframe(data_preview, use_container_width=True)

                            duration = response.get("duration_ms")
                            if duration:
                                st.caption(f"Executed in {duration} ms")

                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": answer,
                                "sql": sql,
                                "duration_ms": duration,
                                "data_preview": data_preview,
                            })
                    except Exception as e:
                        answer = f"Error: {e}"
                        st.error(answer)
                        st.session_state.messages.append({"role": "assistant", "content": answer})

        st.rerun()
