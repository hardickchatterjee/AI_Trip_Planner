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
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 4rem;
    max-width: 760px;
}

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
}
.hero-eyebrow {
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #c9a84c;
    margin-bottom: 0.75rem;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.6rem, 6vw, 3.8rem);
    font-weight: 700;
    color: #f5f0e8;
    line-height: 1.1;
    margin: 0 0 0.6rem;
    letter-spacing: -0.02em;
}
.hero-title span { color: #c9a84c; }
.hero-sub {
    font-size: 0.93rem;
    color: #7a7a8a;
    font-weight: 300;
    max-width: 420px;
    margin: 0 auto;
    line-height: 1.65;
}
.hero-divider {
    width: 48px;
    height: 2px;
    background: linear-gradient(90deg, #c9a84c, transparent);
    margin: 1.4rem auto 0;
    border-radius: 2px;
}

/* ── Input card ── */
.input-card {
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 1.5rem 1.75rem 1.25rem;
    margin: 1.5rem 0 0;
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.05);
}

/* ── Streamlit form border reset ── */
div[data-testid="stForm"] { border: none !important; padding: 0 !important; }

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
    color: #7a7a8a !important;
    font-size: 0.75rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    margin-bottom: 0.4rem !important;
}

/* ── Submit button — full width gold ── */
.stFormSubmitButton { width: 100% !important; margin-top: 0.6rem; }
.stFormSubmitButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #b8940e 0%, #e8c96a 50%, #b8940e 100%) !important;
    background-size: 200% !important;
    color: #0a0f1e !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.7rem 1.5rem !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 20px rgba(201,168,76,0.25) !important;
}
.stFormSubmitButton > button:hover {
    box-shadow: 0 6px 30px rgba(201,168,76,0.45) !important;
    transform: translateY(-1px) !important;
}

/* ── Suggestion pills ── */
.suggestions {
    display: flex;
    flex-wrap: wrap;
    gap: 0.45rem;
    margin: 1rem 0 0;
}
.pill {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.09);
    color: #6a6a7a;
    font-size: 0.76rem;
    padding: 0.28rem 0.8rem;
    border-radius: 20px;
    white-space: nowrap;
}

/* ── Response card header ── */
.resp-header-wrap {
    margin-top: 2rem;
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(201,168,76,0.18);
    border-radius: 16px 16px 0 0;
    overflow: hidden;
    box-shadow: 0 12px 48px rgba(0,0,0,0.4);
    position: relative;
}
.resp-header-wrap::before {
    content: '';
    display: block;
    height: 2px;
    background: linear-gradient(90deg, transparent 0%, #c9a84c 40%, transparent 100%);
}
.resp-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem 1.75rem 0.9rem;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}
.resp-badge {
    background: rgba(201,168,76,0.12);
    color: #c9a84c;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    padding: 0.22rem 0.65rem;
    border-radius: 20px;
    border: 1px solid rgba(201,168,76,0.28);
}
.resp-time {
    font-size: 0.73rem;
    color: #44445a;
    font-weight: 300;
}

/* ── Response body container ── */
.resp-body-wrap {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(201,168,76,0.18);
    border-top: none;
    padding: 1.25rem 1.75rem 0.5rem;
}

/* ── Response footer ── */
.resp-footer-wrap {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(201,168,76,0.18);
    border-top: none;
    border-radius: 0 0 16px 16px;
    padding: 0.6rem 1.75rem 0.9rem;
}
.resp-disclaimer {
    font-size: 0.72rem;
    color: #33334a;
    border-top: 1px solid rgba(255,255,255,0.04);
    padding-top: 0.7rem;
}

/* ── Fix markdown heading colors ── */
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3 {
    font-family: 'Playfair Display', serif !important;
    color: #f0ece2 !important;
    font-weight: 700 !important;
}
[data-testid="stMarkdownContainer"] h1 { font-size: 1.6rem !important; margin-top: 1.25rem !important; }
[data-testid="stMarkdownContainer"] h2 { font-size: 1.25rem !important; margin-top: 1rem !important; }
[data-testid="stMarkdownContainer"] h3 { font-size: 1.05rem !important; margin-top: 0.75rem !important; }
[data-testid="stMarkdownContainer"] p  { color: #a8a49a !important; line-height: 1.75 !important; }
[data-testid="stMarkdownContainer"] li { color: #a8a49a !important; line-height: 1.7 !important; }
[data-testid="stMarkdownContainer"] strong { color: #e8e4da !important; }
[data-testid="stMarkdownContainer"] hr { border-color: rgba(255,255,255,0.07) !important; }

/* ── Spinner ── */
.stSpinner > div { border-top-color: #c9a84c !important; }

/* ── Error ── */
.stAlert {
    background: rgba(200,50,50,0.07) !important;
    border: 1px solid rgba(200,50,50,0.22) !important;
    border-radius: 10px !important;
    color: #d88888 !important;
    margin-top: 1rem;
}

/* ── Footer ── */
.footer {
    text-align: center;
    margin-top: 3rem;
    padding-top: 1.25rem;
    border-top: 1px solid rgba(255,255,255,0.04);
    font-size: 0.68rem;
    color: #2a2a3a;
    letter-spacing: 0.06em;
}
</style>
""", unsafe_allow_html=True)

# ── Hero ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">✦ AI-Powered Travel Planning</div>
    <h1 class="hero-title">Voyager<span>.</span></h1>
    <p class="hero-sub">Tell me where you want to go. I'll craft a personalised itinerary, find hidden gems, and handle every detail.</p>
    <div class="hero-divider"></div>
</div>
""", unsafe_allow_html=True)

# ── Input card ───────────────────────────────────────────────────────────────
st.markdown('<div class="input-card">', unsafe_allow_html=True)

with st.form(key="query_form", clear_on_submit=True):
    user_input = st.text_input(
        "Where are you headed?",
        placeholder="e.g. Plan a 5-day trip to Kyoto in October for 2 people"
    )
    submit_button = st.form_submit_button("✦  Plan My Trip")

st.markdown("""
<div class="suggestions">
    <span class="pill">🏝 Bali, 7 days</span>
    <span class="pill">🏙 Tokyo on a budget</span>
    <span class="pill">🏔 Patagonia trek</span>
    <span class="pill">🌆 NYC weekend</span>
    <span class="pill">🧳 Backpack through Europe</span>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── Response ─────────────────────────────────────────────────────────────────
if submit_button and user_input.strip():
    try:
        with st.spinner("Crafting your itinerary…"):
            payload = {"question": user_input}
            response = requests.post(f"{BASE_URL}/query", json=payload)

        if response.status_code == 200:
            answer = response.json().get("answer", "No answer returned.")
            generated_at = datetime.datetime.now().strftime("%B %d, %Y · %H:%M")

            # Card top + header
            st.markdown(f"""
<div class="resp-header-wrap">
    <div class="resp-header">
        <span class="resp-badge">✦ Your Itinerary</span>
        <span class="resp-time">Generated {generated_at}</span>
    </div>
</div>
<div class="resp-body-wrap">
</div>
""", unsafe_allow_html=True)

            # Native Streamlit markdown (renders headings correctly)
            st.markdown(answer)

            # Card footer
            st.markdown("""
<div class="resp-footer-wrap">
    <div class="resp-disclaimer">
        ✦ AI-generated itinerary — verify prices, hours &amp; travel requirements before booking.
    </div>
</div>
""", unsafe_allow_html=True)

        else:
            st.error(f"The agent couldn't respond right now. Please try again. (Status {response.status_code})")

    except Exception as e:
        st.error(f"Connection failed — is the backend running on port 8000? ({e})")

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">VOYAGER · AI TRAVEL PLANNER · POWERED BY AGENTIC AI</div>
""", unsafe_allow_html=True)