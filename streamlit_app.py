import streamlit as st
import requests
import datetime
import os

# BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8080")
BASE_URL = os.getenv("BACKEND_URL", "http://localhost:8080")
print(f"Using backend URL: {BASE_URL}")

st.set_page_config(
    page_title="Voyager — AI Travel Planner",
    page_icon="✈️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "prefill" not in st.session_state:
    st.session_state.prefill = ""

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --gold:       #c9a84c;
    --gold-light: #e8c96a;
    --gold-dim:   rgba(201,168,76,0.15);
    --bg:         #080c18;
    --surface:    rgba(255,255,255,0.035);
    --border:     rgba(255,255,255,0.07);
    --text:       #e8e4da;
    --muted:      #6a6a7a;
    --dimmer:     #33334a;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg);
    color: var(--text);
}
.stApp {
    background: var(--bg);
    min-height: 100vh;
}
.stApp::before {
    content: '';
    position: fixed; inset: 0; z-index: 0; pointer-events: none;
    background:
        radial-gradient(ellipse 90% 55% at 15% -5%,  rgba(201,168,76,0.09) 0%, transparent 55%),
        radial-gradient(ellipse 70% 45% at 90% 105%, rgba(56,110,180,0.10) 0%, transparent 55%),
        radial-gradient(ellipse 50% 35% at 75%  20%, rgba(180,80,180,0.05) 0%, transparent 50%);
}
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding-top: 0 !important;
    padding-bottom: 5rem;
    max-width: 820px;
    position: relative; z-index: 1;
}

/* ── Form: styled as input card, ghost border removed ── */
div[data-testid="stForm"] {
    border: 1.5px solid rgba(201,168,76,0.45) !important;
    border-radius: 20px !important;
    padding: 1.5rem 1.75rem !important;
    background: linear-gradient(145deg, #111828 0%, #0e1520 100%) !important;
    box-shadow: 0 0 0 4px rgba(201,168,76,0.06), 0 20px 60px rgba(0,0,0,0.5) !important;
    margin-top: 0.5rem !important;
}
/* Only hide truly empty divs - never hide stVerticalBlock */
div[data-testid="stForm"] > div:not([data-testid]):empty {
    display: none !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* ═══════════════════════════════
   HERO
═══════════════════════════════ */
.hero-wrap {
    text-align: center;
    padding: 4.5rem 1rem 2.5rem;
}
.hero-badge {
    display: inline-flex; align-items: center; gap: 0.45rem;
    background: rgba(201,168,76,0.08);
    border: 1px solid rgba(201,168,76,0.2);
    border-radius: 30px;
    padding: 0.28rem 0.9rem;
    font-size: 0.65rem; font-weight: 600;
    letter-spacing: 0.18em; text-transform: uppercase;
    color: var(--gold); margin-bottom: 1.5rem;
}
.hero-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(3.5rem, 9vw, 5.5rem);
    font-weight: 700; color: #f5f0e8;
    line-height: 0.95; margin: 0 0 0.2rem;
    letter-spacing: -0.03em;
}
.hero-title em { color: var(--gold); font-style: italic; }
.hero-tagline {
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(1rem, 2.5vw, 1.35rem);
    color: var(--muted); font-weight: 400; font-style: italic;
    margin: 0.6rem 0 1.75rem;
}
.hero-divider {
    display: flex; align-items: center; justify-content: center; gap: 0.75rem;
}
.hero-divider-line {
    width: 60px; height: 1px;
    background: linear-gradient(90deg, transparent, var(--gold));
}
.hero-divider-line.rev { background: linear-gradient(90deg, var(--gold), transparent); }
.hero-divider-dot { color: var(--gold); font-size: 0.5rem; }

/* ═══════════════════════════════
   STATS BAR
═══════════════════════════════ */
.stats-bar {
    display: flex; justify-content: center;
    margin: 2.5rem 0;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px; overflow: hidden;
    backdrop-filter: blur(10px);
}
.stat-item {
    flex: 1; text-align: center;
    padding: 1.1rem 1rem;
    border-right: 1px solid var(--border);
}
.stat-item:last-child { border-right: none; }
.stat-number {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.9rem; font-weight: 700;
    color: var(--gold-light); line-height: 1; display: block;
}
.stat-label {
    font-size: 0.65rem; color: var(--muted);
    letter-spacing: 0.1em; text-transform: uppercase;
    margin-top: 0.3rem; display: block;
}

/* ═══════════════════════════════
   TICKER
═══════════════════════════════ */
.ticker-wrap {
    overflow: hidden;
    border-top: 1px solid var(--border);
    border-bottom: 1px solid var(--border);
    padding: 0.6rem 0; margin: 0 0 2.5rem;
    background: rgba(201,168,76,0.03);
}
.ticker-inner {
    display: flex; animation: ticker 28s linear infinite;
    white-space: nowrap; width: max-content;
}
.ticker-item {
    font-size: 0.72rem; color: var(--muted);
    letter-spacing: 0.1em; text-transform: uppercase; padding: 0 1.5rem;
}
.ticker-item span { color: var(--gold); margin-right: 0.5rem; }
@keyframes ticker {
    0%   { transform: translateX(0); }
    100% { transform: translateX(-50%); }
}

/* ═══════════════════════════════
   SECTION HEADINGS
═══════════════════════════════ */
.section-heading {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.65rem; font-weight: 600;
    color: #f0ece2; margin: 0 0 0.35rem;
}
.section-sub {
    font-size: 0.82rem; color: var(--muted);
    margin: 0 0 1.25rem; line-height: 1.5;
}

/* ═══════════════════════════════
   DESTINATION CARDS
═══════════════════════════════ */
.dest-grid {
    display: grid; grid-template-columns: repeat(3,1fr);
    gap: 0.85rem; margin-bottom: 2.5rem;
}
.dest-card {
    border-radius: 14px; overflow: hidden;
    border: 1px solid var(--border);
    background: var(--surface); cursor: pointer;
    transition: transform 0.22s, box-shadow 0.22s, border-color 0.22s;
}
.dest-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 16px 40px rgba(0,0,0,0.5);
    border-color: rgba(201,168,76,0.3);
}
.dest-img {
    width: 100%; height: 120px; object-fit: cover;
    display: block; filter: brightness(0.82) saturate(1.1);
    transition: filter 0.22s;
}
.dest-card:hover .dest-img { filter: brightness(0.95) saturate(1.2); }
.dest-info { padding: 0.7rem 0.85rem 0.75rem; }
.dest-name {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.05rem; font-weight: 600; color: #f0ece2; margin: 0 0 0.25rem;
}
.dest-meta { font-size: 0.68rem; color: var(--muted); display: flex; align-items: center; gap: 0.4rem; }
.dest-tag {
    background: var(--gold-dim); color: var(--gold);
    font-size: 0.58rem; font-weight: 600; letter-spacing: 0.08em;
    text-transform: uppercase; padding: 0.12rem 0.45rem; border-radius: 4px;
}

/* ═══════════════════════════════
   HOW IT WORKS
═══════════════════════════════ */
.how-grid {
    display: grid; grid-template-columns: repeat(3,1fr);
    gap: 1rem; margin-bottom: 2.5rem;
}
.how-card {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 14px; padding: 1.4rem 1.1rem 1.3rem; text-align: center;
    transition: border-color 0.2s, transform 0.2s;
}
.how-card:hover { border-color: rgba(201,168,76,0.25); transform: translateY(-2px); }
.how-icon { font-size: 1.6rem; display: block; margin-bottom: 0.75rem; }
.how-step { font-size: 0.6rem; color: var(--gold); letter-spacing: 0.14em; text-transform: uppercase; font-weight: 600; margin-bottom: 0.35rem; }
.how-title { font-family: 'Cormorant Garamond', serif; font-size: 1.05rem; font-weight: 600; color: #f0ece2; margin-bottom: 0.4rem; }
.how-desc { font-size: 0.78rem; color: var(--muted); line-height: 1.55; }

/* ═══════════════════════════════
   TESTIMONIALS
═══════════════════════════════ */
.testi-grid {
    display: grid; grid-template-columns: repeat(3,1fr);
    gap: 0.85rem; margin-bottom: 2.5rem;
}
.testi-card {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 14px; padding: 1.2rem 1.1rem 1.1rem;
    transition: border-color 0.2s;
}
.testi-card:hover { border-color: rgba(201,168,76,0.22); }
.testi-stars { color: var(--gold); font-size: 0.7rem; margin-bottom: 0.6rem; letter-spacing: 0.1em; }
.testi-text {
    font-family: 'Cormorant Garamond', serif;
    font-size: 0.95rem; color: #9a9690; line-height: 1.65;
    font-style: italic; margin-bottom: 0.9rem;
}
.testi-author { font-size: 0.7rem; color: var(--muted); font-weight: 500; }
.testi-author span { color: var(--dimmer); font-weight: 300; margin-left: 0.35rem; }

/* ═══════════════════════════════
   PILL BUTTONS
═══════════════════════════════ */
.pill-label {
    font-size: 0.66rem; color: var(--dimmer);
    letter-spacing: 0.12em; text-transform: uppercase;
    font-weight: 500; margin: 0.5rem 0 0.75rem;
}
div[data-testid="column"] .stButton > button {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    color: #5a5a6a !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.75rem !important; padding: 0.3rem 0.75rem !important;
    border-radius: 20px !important; white-space: nowrap !important;
    transition: all 0.18s ease !important;
    height: auto !important; line-height: 1.5 !important;
    width: 100% !important; min-width: 0 !important;
}
div[data-testid="column"] .stButton > button:hover {
    border-color: rgba(201,168,76,0.45) !important;
    color: var(--gold) !important;
    background: rgba(201,168,76,0.07) !important;
    transform: translateY(-1px) !important;
}

/* INPUT CARD — styles are on div[data-testid="stForm"] above */

.input-card-label {
    font-size: 0.75rem; color: rgba(201,168,76,0.8);
    letter-spacing: 0.14em; text-transform: uppercase;
    font-weight: 600; margin-bottom: 0.5rem;
    display: flex; align-items: center; gap: 0.5rem;
}
.input-card-label::before { content: '✦'; font-size: 0.5rem; }

/* ── Text input inside card — clearly visible ── */
.stTextInput > div > div > input {
    background: #1c2436 !important;
    border: 1.5px solid rgba(255,255,255,0.22) !important;
    border-radius: 12px !important;
    color: #f0ece2 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.85rem 1.1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s, background 0.2s;
    caret-color: var(--gold) !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(201,168,76,0.85) !important;
    box-shadow: 0 0 0 3px rgba(201,168,76,0.12), 0 0 20px rgba(201,168,76,0.08) !important;
    background: #202d42 !important;
    outline: none !important;
}
.stTextInput > div > div > input::placeholder {
    color: #6a7090 !important;
    font-style: italic;
}
/* Hide the default Streamlit label since we render our own */
.stTextInput label { display: none !important; }

/* ── Submit button — full width ── */
.stFormSubmitButton { width: 100% !important; margin-top: 1rem !important; }
.stFormSubmitButton > button {
    display: block !important; width: 100% !important;
    background: linear-gradient(135deg, #a07010 0%, var(--gold-light) 45%, #c9a84c 75%, #a07010 100%) !important;
    background-size: 250% !important;
    color: #06090f !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important; font-size: 0.85rem !important;
    letter-spacing: 0.18em !important; text-transform: uppercase !important;
    border: none !important; border-radius: 12px !important;
    padding: 0.9rem 1.5rem !important; cursor: pointer !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 24px rgba(201,168,76,0.35), 0 1px 0 rgba(255,255,255,0.1) inset !important;
}
.stFormSubmitButton > button:hover {
    box-shadow: 0 8px 40px rgba(201,168,76,0.55) !important;
    transform: translateY(-2px) !important;
    background-position: right center !important;
}

/* ═══════════════════════════════
   CHAT HISTORY
═══════════════════════════════ */
.history-header {
    font-size: 0.66rem; color: var(--dimmer); letter-spacing: 0.1em;
    text-transform: uppercase; font-weight: 500;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    margin: 2rem 0 0.75rem;
}
.chat-user-row { display: flex; justify-content: flex-end; margin: 1rem 0 0.2rem; }
.chat-bubble-user {
    background: rgba(201,168,76,0.1);
    border: 1px solid rgba(201,168,76,0.2);
    border-radius: 14px 14px 4px 14px;
    padding: 0.65rem 1rem; max-width: 78%;
    font-size: 0.9rem; color: #e8c96a; font-weight: 500; line-height: 1.5;
}
.chat-bubble-meta { font-size: 0.62rem; color: #22223a; text-align: right; margin: 0.2rem 0 0; }
.chat-bubble-ai {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(201,168,76,0.13);
    border-radius: 4px 14px 14px 14px;
    overflow: hidden; margin: 0.5rem 0 0;
    box-shadow: 0 4px 24px rgba(0,0,0,0.25);
}
.chat-bubble-ai::before {
    content: ''; display: block; height: 2px;
    background: linear-gradient(90deg, transparent 0%, var(--gold) 40%, transparent 100%);
}
.chat-ai-header {
    display: flex; align-items: center; gap: 0.6rem;
    padding: 0.65rem 1.25rem 0.6rem;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}
.chat-ai-badge {
    background: var(--gold-dim); color: var(--gold);
    font-size: 0.6rem; font-weight: 700; letter-spacing: 0.14em;
    text-transform: uppercase; padding: 0.18rem 0.55rem;
    border-radius: 20px; border: 1px solid rgba(201,168,76,0.22);
}
.chat-ai-time { font-size: 0.65rem; color: #22223a; }
.chat-ai-footer {
    padding: 0.35rem 1.25rem 0.6rem;
    border-top: 1px solid rgba(255,255,255,0.04);
    font-size: 0.64rem; color: #1e1e30;
}

/* ── Markdown ── */
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3 {
    font-family: 'Cormorant Garamond', serif !important;
    color: #f0ece2 !important; font-weight: 600 !important;
}
[data-testid="stMarkdownContainer"] h1 { font-size: 1.55rem !important; margin-top: 1rem !important; }
[data-testid="stMarkdownContainer"] h2 { font-size: 1.25rem !important; margin-top: 0.85rem !important; }
[data-testid="stMarkdownContainer"] h3 { font-size: 1.05rem !important; margin-top: 0.7rem !important; }
[data-testid="stMarkdownContainer"] p  { color: #9a9690 !important; line-height: 1.8 !important; }
[data-testid="stMarkdownContainer"] li { color: #9a9690 !important; line-height: 1.7 !important; }
[data-testid="stMarkdownContainer"] strong { color: #e8e4da !important; }
[data-testid="stMarkdownContainer"] hr { border-color: rgba(255,255,255,0.06) !important; }

/* ── Spinner / error ── */
.stSpinner > div { border-top-color: var(--gold) !important; }
.stAlert {
    background: rgba(200,50,50,0.06) !important;
    border: 1px solid rgba(200,50,50,0.2) !important;
    border-radius: 10px !important; color: #cc8888 !important; margin-top: 1rem;
}

/* ── Clear button ── */
.stButton > button {
    background: transparent !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    color: #2a2a3a !important; font-size: 0.67rem !important;
    padding: 0.18rem 0.55rem !important; border-radius: 6px !important;
    transition: all 0.18s !important;
}
.stButton > button:hover {
    border-color: rgba(180,50,50,0.28) !important;
    color: #774040 !important;
}

/* ── Footer ── */
.footer-wrap {
    text-align: center; margin-top: 4rem;
    padding: 2rem 0 1rem;
    border-top: 1px solid rgba(255,255,255,0.04);
}
.footer-logo {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.3rem; font-weight: 700;
    color: rgba(201,168,76,0.35); letter-spacing: 0.12em; margin-bottom: 0.5rem;
}
.footer-copy { font-size: 0.64rem; color: #1e1e30; letter-spacing: 0.06em; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  HERO
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-wrap">
    <div class="hero-badge">✦ AI-Powered Travel Planning</div>
    <h1 class="hero-title">Voy<em>ager</em></h1>
    <p class="hero-tagline">Your world, curated by intelligence.</p>
    <div class="hero-divider">
        <div class="hero-divider-line"></div>
        <span class="hero-divider-dot">✦</span>
        <div class="hero-divider-line rev"></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  STATS BAR
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="stats-bar">
    <div class="stat-item"><span class="stat-number">42K+</span><span class="stat-label">Itineraries crafted</span></div>
    <div class="stat-item"><span class="stat-number">190+</span><span class="stat-label">Countries covered</span></div>
    <div class="stat-item"><span class="stat-number">4.9★</span><span class="stat-label">Avg. traveller rating</span></div>
    <div class="stat-item"><span class="stat-number">&lt;10s</span><span class="stat-label">Plan generation time</span></div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  TICKER
# ═══════════════════════════════════════════════════════════════════════════════
ticker_items = [
    "🗼 Paris","🏯 Kyoto","🌴 Bali","🏔 Patagonia","🦁 Serengeti",
    "🕌 Marrakech","🏝 Maldives","🗽 New York","🏛 Athens","🌸 Seoul",
    "🎭 Buenos Aires","🏔 Nepal","🌊 Amalfi Coast","🐘 Sri Lanka","🌅 Santorini",
]
ticker_html = "".join([f'<span class="ticker-item"><span>✦</span>{t}</span>' for t in ticker_items * 2])
st.markdown(f'<div class="ticker-wrap"><div class="ticker-inner">{ticker_html}</div></div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  DESTINATIONS
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<p class="section-heading">Trending Destinations</p>', unsafe_allow_html=True)
st.markdown('<p class="section-sub">Handpicked by our AI from thousands of traveller journeys this season.</p>', unsafe_allow_html=True)

destinations = [
    {"name":"Kyoto, Japan",    "img":"https://images.unsplash.com/photo-1545569341-9eb8b30979d9?w=400&q=80","tag":"Culture",   "meta":"7–10 days · Oct–Nov"},
    {"name":"Amalfi Coast",    "img":"https://images.unsplash.com/photo-1612698093158-e07ac200d44e?w=400&q=80","tag":"Scenic",    "meta":"5–7 days · May–Sep"},
    {"name":"Bali, Indonesia", "img":"https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=400&q=80","tag":"Wellness",  "meta":"7–14 days · Apr–Oct"},
    {"name":"Patagonia",       "img":"https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=400&q=80","tag":"Adventure", "meta":"10–14 days · Nov–Mar"},
    {"name":"Marrakech",       "img":"https://images.unsplash.com/photo-1539020140153-e479b8c22e70?w=400&q=80","tag":"Culture",   "meta":"4–6 days · Mar–May"},
    {"name":"Santorini",       "img":"https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?w=400&q=80","tag":"Romance",   "meta":"4–7 days · Jun–Sep"},
]
cards_html = '<div class="dest-grid">'
for d in destinations:
    cards_html += f"""<div class="dest-card">
        <img class="dest-img" src="{d['img']}" alt="{d['name']}" loading="lazy"/>
        <div class="dest-info">
            <div class="dest-name">{d['name']}</div>
            <div class="dest-meta"><span class="dest-tag">{d['tag']}</span>{d['meta']}</div>
        </div></div>"""
st.markdown(cards_html + "</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  HOW IT WORKS
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<p class="section-heading">How Voyager Works</p>', unsafe_allow_html=True)
st.markdown('<p class="section-sub">From a single prompt to a complete, personalised itinerary in seconds.</p>', unsafe_allow_html=True)
st.markdown("""
<div class="how-grid">
    <div class="how-card"><span class="how-icon">🗺️</span><div class="how-step">Step 01</div><div class="how-title">Tell us your dream</div><div class="how-desc">Type your destination, duration, budget, or travel style — as specific or vague as you like.</div></div>
    <div class="how-card"><span class="how-icon">🤖</span><div class="how-step">Step 02</div><div class="how-title">AI crafts your plan</div><div class="how-desc">Our agent researches hotels, attractions, restaurants, transport and weather in real time.</div></div>
    <div class="how-card"><span class="how-icon">✈️</span><div class="how-step">Step 03</div><div class="how-title">Pack &amp; go</div><div class="how-desc">Get a day-by-day itinerary with cost breakdowns, tips, and alternatives — ready to use.</div></div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  PLAN YOUR TRIP — PILLS + INPUT
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<p class="section-heading" style="margin-top:2.5rem">Plan Your Trip</p>', unsafe_allow_html=True)
st.markdown('<p class="pill-label" style="margin-bottom:0.75rem">Quick start — tap a destination</p>', unsafe_allow_html=True)

PILLS = [
    ("🏝", "Plan a 7-day trip to Bali"),
    ("🏙", "Plan a budget trip to Tokyo"),
    ("🏔", "Plan a Patagonia trekking trip"),
    ("🌆", "Plan a NYC weekend getaway"),
    ("🧳", "Backpacking itinerary through Europe"),
]
PILL_LABELS = ["🏝 Bali 7d", "🏙 Tokyo budget", "🏔 Patagonia", "🌆 NYC weekend", "🧳 Europe"]

cols = st.columns(len(PILLS))
for i, (col, (_, query_text), label) in enumerate(zip(cols, PILLS, PILL_LABELS)):
    with col:
        if st.button(label, key=f"pill_{i}"):
            st.session_state.prefill = query_text
            st.rerun()

st.markdown('<p class="input-card-label" style="margin-top:1.25rem">Where are you headed?</p>', unsafe_allow_html=True)

with st.form(key="query_form", clear_on_submit=True):
    user_input = st.text_input(
        label="destination_input",
        label_visibility="hidden",
        value=st.session_state.prefill,
        placeholder="e.g. 5 days in Kyoto for 2 people, mid-range budget",
    )
    submit_button = st.form_submit_button("✦  Generate My Itinerary")

# ═══════════════════════════════════════════════════════════════════════════════
#  CHAT HISTORY — right after input so itinerary feels like a chat reply
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state.chat_history:
    col_label, col_clear = st.columns([6, 1])
    with col_label:
        st.markdown('<div class="history-header">✦ Your Conversation History</div>', unsafe_allow_html=True)
    with col_clear:
        st.markdown("<div style='margin-top:1.85rem'></div>", unsafe_allow_html=True)
        if st.button("✕ Clear", key="clear_history"):
            st.session_state.chat_history = []
            st.rerun()

    for entry in st.session_state.chat_history:
        st.markdown(f"""
<div class="chat-user-row">
    <div>
        <div class="chat-bubble-user">🧳 {entry['question']}</div>
        <div class="chat-bubble-meta">{entry['time']}</div>
    </div>
</div>""", unsafe_allow_html=True)

        st.markdown(f"""
<div class="chat-bubble-ai">
    <div class="chat-ai-header">
        <span class="chat-ai-badge">✦ Itinerary</span>
        <span class="chat-ai-time">{entry['time']}</span>
    </div>
    <div style="padding:0.75rem 1.25rem 0.25rem">
</div>""", unsafe_allow_html=True)
        st.markdown(entry['answer'])
        st.markdown("""
<div class="chat-ai-footer">✦ AI-generated — verify prices &amp; requirements before booking.</div>
</div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  TESTIMONIALS — static footer content, always below chat
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("<div style='margin-top:3rem'></div>", unsafe_allow_html=True)
st.markdown('<p class="section-heading">What Travellers Say</p>', unsafe_allow_html=True)
st.markdown('<p class="section-sub">Real experiences from Voyager users around the world.</p>', unsafe_allow_html=True)
st.markdown("""
<div class="testi-grid">
    <div class="testi-card">
        <div class="testi-stars">★★★★★</div>
        <div class="testi-text">"Planned our entire 10-day Japan trip in under a minute. The off-beat recommendations were things no travel blog had ever mentioned."</div>
        <div class="testi-author">Priya M. <span>· Mumbai, India</span></div>
    </div>
    <div class="testi-card">
        <div class="testi-stars">★★★★★</div>
        <div class="testi-text">"The cost breakdown was shockingly accurate. Saved us hundreds by booking exactly what the AI suggested. Will never travel without this."</div>
        <div class="testi-author">James T. <span>· London, UK</span></div>
    </div>
    <div class="testi-card">
        <div class="testi-stars">★★★★☆</div>
        <div class="testi-text">"Asked for a solo backpacking route through Southeast Asia. Got a masterpiece — complete with visa tips and local transport hacks."</div>
        <div class="testi-author">Sofia R. <span>· São Paulo, Brazil</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  HANDLE SUBMISSION
# ═══════════════════════════════════════════════════════════════════════════════
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
        st.error(f"Connection failed — is the backend running on port 8080? ({e}) {BASE_URL}")

# ═══════════════════════════════════════════════════════════════════════════════
#  FOOTER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="footer-wrap">
    <div class="footer-logo">VOYAGER</div>
    <div class="footer-copy">© 2026 · AI TRAVEL PLANNER · POWERED BY AGENTIC AI · ALL RIGHTS RESERVED</div>
</div>
""", unsafe_allow_html=True)