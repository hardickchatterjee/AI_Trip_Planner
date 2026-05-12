import streamlit as st
import requests
import datetime

BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Voyager — AI Travel Planner",
    page_icon="✈️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Session state ────────────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "prefill" not in st.session_state:
    st.session_state.prefill = ""

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0a0f1e;
    color: #e8e4da;
}
.stApp {
    background:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(255,180,60,0.10) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 85% 110%, rgba(70,130,180,0.12) 0%, transparent 60%),
        #0a0f1e;
    min-height: 100vh;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem; padding-bottom: 4rem; max-width: 780px; }

/* ── Remove ALL blank gaps from Streamlit internals ── */
div[data-testid="stForm"] {
    border: none !important;
    padding: 0 !important;
    background: transparent !important;
}
div[data-testid="stForm"] > div:first-child { margin-top: 0 !important; padding-top: 0 !important; }
.element-container { margin-bottom: 0 !important; }
div[data-testid="stVerticalBlock"] > div { gap: 0 !important; }

/* ── Hero ── */
.hero { text-align: center; padding: 2.5rem 1rem 1.5rem; }
.hero-eyebrow {
    font-size: 0.68rem; font-weight: 500; letter-spacing: 0.22em;
    text-transform: uppercase; color: #c9a84c; margin-bottom: 0.75rem;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.6rem, 6vw, 3.8rem); font-weight: 700;
    color: #f5f0e8; line-height: 1.1; margin: 0 0 0.6rem; letter-spacing: -0.02em;
}
.hero-title span { color: #c9a84c; }
.hero-sub {
    font-size: 0.93rem; color: #7a7a8a; font-weight: 300;
    max-width: 420px; margin: 0 auto; line-height: 1.65;
}
.hero-divider {
    width: 48px; height: 2px;
    background: linear-gradient(90deg, #c9a84c, transparent);
    margin: 1.4rem auto 0; border-radius: 2px;
}

/* ── Suggestion label ── */
.suggestion-label {
    font-size: 0.68rem; color: #44445a; letter-spacing: 0.12em;
    text-transform: uppercase; margin: 1.5rem 0 0.6rem;
    font-weight: 500;
}

/* ── Pill buttons — override Streamlit defaults ── */
div[data-testid="column"] .stButton > button {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    color: #6a6a7a !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.78rem !important;
    padding: 0.32rem 0.85rem !important;
    border-radius: 20px !important;
    white-space: nowrap !important;
    transition: all 0.18s ease !important;
    height: auto !important;
    line-height: 1.5 !important;
    width: 100% !important;
    min-width: 0 !important;
}
div[data-testid="column"] .stButton > button:hover {
    border-color: rgba(201,168,76,0.45) !important;
    color: #c9a84c !important;
    background: rgba(201,168,76,0.07) !important;
    transform: translateY(-1px) !important;
}

/* ── Input card ── */
.input-card {
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.4rem 1.6rem 1.3rem;
    margin: 0.75rem 0 0;
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.05);
}

/* ── Text input ── */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.11) !important;
    border-radius: 10px !important;
    color: #f0ece2 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.72rem 1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.stTextInput > div > div > input:focus {
    border-color: #c9a84c !important;
    box-shadow: 0 0 0 3px rgba(201,168,76,0.12) !important;
    outline: none !important;
}
.stTextInput > div > div > input::placeholder { color: #44445a !important; }
.stTextInput label {
    color: #7a7a8a !important; font-size: 0.75rem !important;
    font-weight: 500 !important; letter-spacing: 0.1em !important;
    text-transform: uppercase !important; margin-bottom: 0.35rem !important;
    display: block !important;
}

/* ── Submit button — full width ── */
.stFormSubmitButton { width: 100% !important; margin-top: 0.75rem !important; }
.stFormSubmitButton > button {
    display: block !important;
    width: 100% !important;
    background: linear-gradient(135deg, #b8940e 0%, #e8c96a 50%, #b8940e 100%) !important;
    background-size: 200% !important;
    color: #0a0f1e !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important; font-size: 0.85rem !important;
    letter-spacing: 0.14em !important; text-transform: uppercase !important;
    border: none !important; border-radius: 10px !important;
    padding: 0.78rem 1.5rem !important; cursor: pointer !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 20px rgba(201,168,76,0.28) !important;
}
.stFormSubmitButton > button:hover {
    box-shadow: 0 6px 30px rgba(201,168,76,0.48) !important;
    transform: translateY(-1px) !important;
}

/* ── Chat history section ── */
.history-label {
    font-size: 0.68rem; color: #33334a; letter-spacing: 0.1em;
    text-transform: uppercase; margin: 2rem 0 0.75rem;
    font-weight: 500; padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}

/* ── User bubble ── */
.chat-user-row { display: flex; justify-content: flex-end; margin: 1rem 0 0.25rem; }
.chat-bubble-user {
    background: rgba(201,168,76,0.11);
    border: 1px solid rgba(201,168,76,0.22);
    border-radius: 14px 14px 4px 14px;
    padding: 0.65rem 1rem;
    max-width: 78%;
    font-size: 0.9rem; color: #e8c96a; font-weight: 500; line-height: 1.5;
}
.chat-bubble-meta {
    font-size: 0.63rem; color: #2a2a3a;
    text-align: right; margin: 0.2rem 0 0; letter-spacing: 0.04em;
}

/* ── AI bubble ── */
.chat-bubble-ai {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(201,168,76,0.14);
    border-radius: 4px 14px 14px 14px;
    overflow: hidden;
    box-shadow: 0 4px 24px rgba(0,0,0,0.28);
    margin: 0.5rem 0 0;
    position: relative;
}
.chat-bubble-ai::before {
    content: '';
    display: block; height: 2px;
    background: linear-gradient(90deg, transparent 0%, #c9a84c 40%, transparent 100%);
}
.chat-ai-header {
    display: flex; align-items: center; gap: 0.6rem;
    padding: 0.65rem 1.25rem 0.6rem;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}
.chat-ai-badge {
    background: rgba(201,168,76,0.11); color: #c9a84c;
    font-size: 0.62rem; font-weight: 700; letter-spacing: 0.14em;
    text-transform: uppercase; padding: 0.18rem 0.55rem;
    border-radius: 20px; border: 1px solid rgba(201,168,76,0.25);
}
.chat-ai-time { font-size: 0.67rem; color: #33334a; font-weight: 300; }
.chat-ai-body  { padding: 0.75rem 1.25rem 0.25rem; }
.chat-ai-footer {
    padding: 0.35rem 1.25rem 0.6rem;
    border-top: 1px solid rgba(255,255,255,0.04);
    font-size: 0.66rem; color: #2a2a3a;
}

/* ── Markdown overrides ── */
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3 {
    font-family: 'Playfair Display', serif !important;
    color: #f0ece2 !important; font-weight: 700 !important;
}
[data-testid="stMarkdownContainer"] h1 { font-size: 1.4rem !important; margin-top: 1rem !important; }
[data-testid="stMarkdownContainer"] h2 { font-size: 1.15rem !important; margin-top: 0.85rem !important; }
[data-testid="stMarkdownContainer"] h3 { font-size: 1rem !important; margin-top: 0.7rem !important; }
[data-testid="stMarkdownContainer"] p  { color: #a8a49a !important; line-height: 1.75 !important; }
[data-testid="stMarkdownContainer"] li { color: #a8a49a !important; line-height: 1.7 !important; }
[data-testid="stMarkdownContainer"] strong { color: #e8e4da !important; }
[data-testid="stMarkdownContainer"] hr { border-color: rgba(255,255,255,0.07) !important; }

/* ── Clear button ── */
.stButton.clear > button {
    background: transparent !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    color: #2a2a3a !important; font-size: 0.67rem !important;
    padding: 0.18rem 0.55rem !important; border-radius: 6px !important;
}
.stButton.clear > button:hover {
    border-color: rgba(180,50,50,0.3) !important;
    color: #884444 !important;
}

/* ── Spinner ── */
.stSpinner > div { border-top-color: #c9a84c !important; }

/* ── Error ── */
.stAlert {
    background: rgba(200,50,50,0.07) !important;
    border: 1px solid rgba(200,50,50,0.22) !important;
    border-radius: 10px !important; color: #d88888 !important; margin-top: 1rem;
}

/* ── Footer ── */
.footer {
    text-align: center; margin-top: 3rem; padding-top: 1.25rem;
    border-top: 1px solid rgba(255,255,255,0.04);
    font-size: 0.67rem; color: #22223a; letter-spacing: 0.07em;
}
</style>
""", unsafe_allow_html=True)

# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">✦ AI-Powered Travel Planning</div>
    <h1 class="hero-title">Voyager<span>.</span></h1>
    <p class="hero-sub">Tell me where you want to go. I'll craft a personalised itinerary, find hidden gems, and handle every detail.</p>
    <div class="hero-divider"></div>
</div>
""", unsafe_allow_html=True)

# ── Chat history ─────────────────────────────────────────────────────────────
if st.session_state.chat_history:
    col_label, col_clear = st.columns([6, 1])
    with col_label:
        st.markdown('<div class="history-label">✦ Conversation History</div>', unsafe_allow_html=True)
    with col_clear:
        st.markdown("<div style='margin-top:1.9rem'></div>", unsafe_allow_html=True)
        if st.button("✕ Clear", key="clear_history"):
            st.session_state.chat_history = []
            st.rerun()

    for entry in st.session_state.chat_history:
        # User bubble
        st.markdown(f"""
<div class="chat-user-row">
    <div>
        <div class="chat-bubble-user">🧳 {entry['question']}</div>
        <div class="chat-bubble-meta">{entry['time']}</div>
    </div>
</div>
""", unsafe_allow_html=True)

        # AI bubble — header
        st.markdown(f"""
<div class="chat-bubble-ai">
    <div class="chat-ai-header">
        <span class="chat-ai-badge">✦ Itinerary</span>
        <span class="chat-ai-time">{entry['time']}</span>
    </div>
    <div class="chat-ai-body">
</div>
""", unsafe_allow_html=True)

        st.markdown(entry['answer'])  # native render — correct heading colors

        st.markdown("""
<div class="chat-ai-footer">✦ AI-generated — verify prices &amp; requirements before booking.</div>
</div>
""", unsafe_allow_html=True)

# ── Suggestion pills (ABOVE input) ───────────────────────────────────────────
PILLS = [
    ("🏝", "Plan a 7-day trip to Bali"),
    ("🏙", "Plan a budget trip to Tokyo"),
    ("🏔", "Plan a Zion national park trekking trip"),
    ("🌆", "Plan a NYC weekend getaway"),
    ("🧳", "Backpacking itinerary through Europe"),
]
PILL_LABELS = ["🏝 Bali, 7 days", "🏙 Tokyo budget", "🏔 Zion trekking", "🌆 NYC weekend", "🧳 Europe trip"]

st.markdown('<div class="suggestion-label">Quick start — pick a destination</div>', unsafe_allow_html=True)

cols = st.columns(len(PILLS))
for i, (col, (_, query_text), label) in enumerate(zip(cols, PILLS, PILL_LABELS)):
    with col:
        if st.button(label, key=f"pill_{i}"):
            st.session_state.prefill = query_text
            st.rerun()

# ── Input card ────────────────────────────────────────────────────────────────
st.markdown('<div class="input-card">', unsafe_allow_html=True)

with st.form(key="query_form", clear_on_submit=True):
    user_input = st.text_input(
        "Where are you headed?",
        value=st.session_state.prefill,
        placeholder="e.g. Plan a 5-day trip to Kyoto in October for 2 people",
    )
    submit_button = st.form_submit_button("✦  Plan My Trip")

st.markdown('</div>', unsafe_allow_html=True)

# ── Handle submission ─────────────────────────────────────────────────────────
query = user_input.strip() if submit_button and user_input.strip() else ""

if query:
    st.session_state.prefill = ""
    try:
        with st.spinner("Crafting your itinerary…"):
            response = requests.post(f"{BASE_URL}/query", json={"question": query})

        if response.status_code == 200:
            answer = response.json().get("answer", "No answer returned.")
            st.session_state.chat_history.append({
                "question": query,
                "answer":   answer,
                "time":     datetime.datetime.now().strftime("%b %d, %Y · %H:%M"),
            })
            st.rerun()
        else:
            st.error(f"The agent couldn't respond. (Status {response.status_code})")

    except Exception as e:
        st.error(f"Connection failed — is the backend running on port 8000? ({e})")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown('<div class="footer">VOYAGER · AI TRAVEL PLANNER · POWERED BY AGENTIC AI</div>', unsafe_allow_html=True)