import streamlit as st
import numpy as np
import pandas as pd
import joblib
import os
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="SMARTPRICE AI",
    page_icon="🚀",
    layout="centered"
)

#css
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800;900&family=Poppins:wght@300;400;600;700&display=swap');

html, body, [class*="css"]  {
    font-family: 'Poppins', sans-serif;
    background: radial-gradient(circle at top left, #0F172A, #020617 60%);
    color: #E2E8F0;
}

#MainMenu, footer, header {visibility: hidden;}

.block-container {
    padding: 2rem 2rem 3rem;
    max-width: 850px;
}

.hero {
    text-align: center;
    padding: 3.5rem 1rem;
    border-radius: 24px;
    background: linear-gradient(145deg, #060D1F, #0D1525, #0F172A);
    box-shadow: 0 0 80px rgba(56,189,248,0.15), 0 0 140px rgba(99,102,241,0.1), inset 0 1px 0 rgba(255,255,255,0.05);
    border: 1px solid rgba(56,189,248,0.3);
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::after {
    content: '';
    position: absolute;
    top: -60%;
    left: 50%;
    transform: translateX(-50%);
    width: 70%;
    height: 120%;
    background: radial-gradient(ellipse, rgba(99,102,241,0.08) 0%, transparent 70%);
    pointer-events: none;
}

.brand {
    font-family: 'Orbitron', sans-serif;
    font-size: 3.2rem;
    font-weight: 900;
    letter-spacing: 4px;
    background: linear-gradient(90deg, #38BDF8, #6366F1, #A78BFA, #38BDF8);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: none;
    filter: drop-shadow(0 0 20px rgba(56,189,248,0.4));
}

.tagline {
    margin-top: 10px;
    font-size: 0.85rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #64748B;
}

.team {
    display:inline-block;
    padding:6px 18px;
    border-radius:30px;
    border:1px solid #38BDF8;
    color:#38BDF8;
    font-size:0.7rem;
    letter-spacing:2px;
    margin-bottom:15px;
}

.section-label {
    font-family: 'Orbitron', sans-serif;
    font-size: 0.8rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #38BDF8;
    margin: 1.5rem 0 1rem;
}

div[data-testid="stButton"] > button {
    background: linear-gradient(135deg,#0EA5E9,#6366F1);
    border-radius: 12px;
    padding: 0.8rem 2rem;
    font-weight: 700;
    border: none;
    transition: 0.3s ease;
    box-shadow: 0 6px 25px rgba(99,102,241,0.4);
}
div[data-testid="stButton"] > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 35px rgba(99,102,241,0.6);
}

div[data-testid="stMetric"] {
    background: linear-gradient(145deg, rgba(14,165,233,0.08), rgba(99,102,241,0.12));
    border: 1px solid rgba(56,189,248,0.4);
    border-radius: 15px;
    padding: 1.2rem !important;
    box-shadow: 0 0 25px rgba(56,189,248,0.12), inset 0 1px 0 rgba(255,255,255,0.05);
    backdrop-filter: blur(10px);
    transition: 0.3s;
}
div[data-testid="stMetric"]:hover {
    border-color: rgba(99,102,241,0.8);
    box-shadow: 0 0 40px rgba(99,102,241,0.35), inset 0 1px 0 rgba(255,255,255,0.08);
    transform: translateY(-2px);
}
</style>

<div class="hero">
    <div class="team">TEAM RUDRAKSHA</div>
    <div class="brand">SMARTPRICE AI</div>
    <div class="tagline">Machine Learning · NEPSE Intelligence · Predictive Analytics</div>
</div>
""", unsafe_allow_html=True)

STOCKS = {
    'Nabil Bank':               {'close': 'models/model_nabil.pkl',       'high': 'models/model_nabil_high.pkl',       'low': 'models/model_nabil_low.pkl'},
    'Nepal Doorsanchar':        {'close': 'models/model_doorsanchar.pkl', 'high': 'models/model_doorsanchar_high.pkl', 'low': 'models/model_doorsanchar_low.pkl'},
    'Citizen Investment Trust': {'close': 'models/model_citizen.pkl',     'high': 'models/model_citizen_high.pkl',     'low': 'models/model_citizen_low.pkl'},
}

FEATURES = ['PREV_CLOSE', 'MA_5', 'MA_10', 'DAILY_RANGE', 'MOMENTUM', 'PREV_HIGH', 'PREV_LOW']

def load_model(path):
    if not os.path.exists(path):
        return None
    return joblib.load(path)

st.markdown('<div class="section-label">Select Stock</div>', unsafe_allow_html=True)
stock_name  = st.selectbox("", list(STOCKS.keys()), label_visibility="collapsed")
info        = STOCKS[stock_name]
model_close = load_model(info['close'])
model_high  = load_model(info['high'])
model_low   = load_model(info['low'])

if not model_close:
    st.error("❌ Model not found. Run notebook and save models first.")
    st.stop()

if not model_high or not model_low:
    st.warning("⚠️ High/Low models not found. Run Cell 46 in notebook.")

st.divider()

st.markdown('<div class="section-label">Enter Today\'s Data</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    prev_close = st.number_input("Today's Close (Rs.)",    min_value=1.0, value=500.0, step=0.5)
    high       = st.number_input("Today's High (Rs.)",     min_value=1.0, value=510.0, step=0.5)
    low        = st.number_input("Today's Low (Rs.)",      min_value=1.0, value=490.0, step=0.5)
    prev_high  = st.number_input("Yesterday's High (Rs.)", min_value=1.0, value=512.0, step=0.5)
with col2:
    prev_low   = st.number_input("Yesterday's Low (Rs.)",  min_value=1.0, value=488.0, step=0.5)
    ma5        = st.number_input("5-Day Moving Avg (Rs.)", min_value=1.0, value=498.0, step=0.5)
    ma10       = st.number_input("10-Day Mov. Avg (Rs.)",  min_value=1.0, value=495.0, step=0.5)
    momentum   = st.number_input("Momentum (Close−6d)",    value=5.0,     step=0.5)

daily_range = high - low
st.info(f"Daily Range (auto-calculated): **Rs. {daily_range:.2f}**")

st.divider()

if st.button("Predict Tomorrow's Prices →", use_container_width=True):
    X = np.array([[prev_close, ma5, ma10, daily_range, momentum, prev_high, prev_low]])

    pred_close = model_close.predict(X)[0]
    pred_high  = model_high.predict(X)[0] if model_high else pred_close * 1.01
    pred_low   = model_low.predict(X)[0]  if model_low  else pred_close * 0.99
    pred_range = pred_high - pred_low
    change     = pred_close - prev_close
    change_pct = (change / prev_close) * 100
    mae_approx = 5.0
    conf_low   = pred_close - mae_approx
    conf_high  = pred_close + mae_approx

    st.markdown(f'<div class="section-label">Tomorrow\'s Predictions — {stock_name}</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("Predicted Close", f"Rs. {pred_close:.2f}", f"{change:+.2f} ({change_pct:+.2f}%)")
    c2.metric("Predicted High",  f"Rs. {pred_high:.2f}",  f"+{pred_high - prev_close:.2f}")
    c3.metric("Predicted Low",   f"Rs. {pred_low:.2f}",   f"{pred_low - prev_close:+.2f}")

    st.info(f"📊 Confidence Range: **Rs. {conf_low:.2f} – Rs. {conf_high:.2f}**  *(close ± {mae_approx} NPR)*")

    st.divider()

    #                                  GRAPH 
    today     = [prev_close, high, low]
    tomorrow  = [pred_close, pred_high, pred_low]
    labels    = ['Close', 'High', 'Low']

    plt.figure(figsize=(12, 4))
    plt.plot(labels, today,    label='Today',     color='blue')
    plt.plot(labels, tomorrow, label='Tomorrow',  color='red', linestyle='--')
    plt.title(f'{stock_name} — Today vs Tomorrow Predicted')
    plt.ylabel('Price (Rs.)')
    plt.legend()
    plt.tight_layout()
    st.pyplot(plt)
    plt.close()

    st.divider()

    st.markdown('<div class="section-label">Full Summary</div>', unsafe_allow_html=True)
    summary = pd.DataFrame({
        'Price Point':              ['High', 'Low', 'Close', 'Range'],
        'Today (Rs.)':              [f"{high:.2f}", f"{low:.2f}", f"{prev_close:.2f}", f"{daily_range:.2f}"],
        'Tomorrow Predicted (Rs.)': [f"{pred_high:.2f}", f"{pred_low:.2f}", f"{pred_close:.2f}", f"{pred_range:.2f}"],
    })
    st.dataframe(summary, use_container_width=True, hide_index=True)

    st.divider()

    if change > 0:
        st.success(f"📈 BUY Signal — Price expected to rise by Rs. {change:.2f} ({change_pct:+.2f}%)")
       
    else:
        st.error(f"📉 SELL Signal — Price expected to fall by Rs. {abs(change):.2f} ({change_pct:+.2f}%)")
        
    st.markdown("""
        <div style="text-align:center; margin-top:1rem; font-size:0.75rem; color:#64748B;">
        ⚠️ SmartPrice AI is an ML-based tool. Predictions may not be accurate. 
        Always do your own research before investing.
        </div>
        """, unsafe_allow_html=True)
    st.divider()


# ── FEEDBACK SYSTEM 
import datetime, pytz, requests, base64, json

GITHUB_TOKEN  = st.secrets["GITHUB_TOKEN"]
GITHUB_REPO   = st.secrets["GITHUB_REPO"]
FEEDBACK_FILE = "feedbacks.txt"
NPT           = pytz.timezone("Asia/Kathmandu")

def github_get_file():
    url     = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{FEEDBACK_FILE}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        data    = r.json()
        content = base64.b64decode(data["content"]).decode("utf-8")
        return content, data["sha"]
    return "", None

def load_feedbacks():
    try:
        content, _ = github_get_file()
        if not content.strip():
            return []
        entries   = content.strip().split("---ENTRY---")
        feedbacks = []
        for entry in entries:
            if entry.strip():
                fb = {}
                for line in entry.strip().split("\n"):
                    if line.startswith("NAME:"):    fb["name"]    = line[5:].strip()
                    if line.startswith("RATING:"):  fb["rating"]  = line[7:].strip()
                    if line.startswith("COMMENT:"): fb["comment"] = line[8:].strip()
                    if line.startswith("TIME:"):    fb["time"]    = line[5:].strip()
                if fb:
                    feedbacks.append(fb)
        return feedbacks
    except:
        return []

def save_feedback(name, rating, comment):
    try:
        existing, sha = github_get_file()
        time_str  = datetime.datetime.now(NPT).strftime("%d %b %Y, %I:%M %p")
        new_entry = f"NAME:{name}\nRATING:{rating}\nCOMMENT:{comment}\nTIME:{time_str}"
        updated   = (existing.strip() + "\n---ENTRY---\n" + new_entry).strip()
        encoded   = base64.b64encode(updated.encode("utf-8")).decode("utf-8")
        url       = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{FEEDBACK_FILE}"
        headers   = {"Authorization": f"token {GITHUB_TOKEN}", "Content-Type": "application/json"}
        payload   = {"message": f"feedback: {name}", "content": encoded}
        if sha:
            payload["sha"] = sha
        r = requests.put(url, headers=headers, data=json.dumps(payload))
        return r.status_code in [200, 201]
    except Exception as e:
        st.error(f"Could not save: {e}")
        return False

st.markdown('<div class="section-label">Leave a Feedback</div>', unsafe_allow_html=True)

import streamlit.components.v1 as components

# Check localStorage for submitted flag
check_html = """
<script>
    const done = localStorage.getItem('smartprice_fb_done');
    // Send value back to Streamlit via URL param
    const url = new URL(window.location.href);
    if (done === '1' && !url.searchParams.get('fb_done')) {
        url.searchParams.set('fb_done', '1');
        window.history.replaceState({}, '', url.toString());
        window.location.reload();
    }
</script>
"""
components.html(check_html, height=0)

# 
fb_done = st.query_params.get("fb_done", "0") == "1"

if fb_done:
    st.markdown("""
    <div style="background:linear-gradient(135deg,rgba(99,102,241,0.15),rgba(56,189,248,0.1));
        border:1px solid rgba(99,102,241,0.4); border-radius:14px; padding:1.2rem;
        text-align:center; color:#A78BFA; font-weight:600; font-size:0.95rem;">
        ✅ You have already submitted your feedback from this device. Thank you!
    </div>
    """, unsafe_allow_html=True)
else:
    with st.form("feedback_form", clear_on_submit=True):
        fb_col1, fb_col2 = st.columns(2)
        with fb_col1:
            fb_name   = st.text_input("Your Name", placeholder="e.g. Aarav Sharma")
        with fb_col2:
            fb_rating = st.selectbox("Rating", ["⭐⭐⭐⭐⭐ Excellent", "⭐⭐⭐⭐ Good", "⭐⭐⭐ Average", "⭐⭐ Poor", "⭐ Very Poor"])
        fb_comment = st.text_area("Your Feedback", placeholder="Share your experience with SMARTPRICE AI...", height=100)
        submitted  = st.form_submit_button("Submit Feedback →", use_container_width=True)

        if submitted:
            if fb_name.strip() and fb_comment.strip():
                with st.spinner("Saving..."):
                    if save_feedback(fb_name.strip(), fb_rating, fb_comment.strip()):
                        # Set localStorage flag permanently on this device
                        components.html("""
                        <script>
                            localStorage.setItem('smartprice_fb_done', '1');
                            const url = new URL(window.location.href);
                            url.searchParams.set('fb_done', '1');
                            window.history.replaceState({}, '', url.toString());
                            window.location.reload();
                        </script>
                        """, height=0)
                        st.success("✅ Thank you! Your feedback is now visible to everyone.")
                        st.rerun()
            else:
                st.warning("⚠️ Please enter your name and feedback.")

feedbacks = load_feedbacks()
if feedbacks:
    st.markdown(f'<div class="section-label">All Feedbacks ({len(feedbacks)})</div>', unsafe_allow_html=True)
    for fb in reversed(feedbacks):
        st.markdown(f"""
        <div style="
            background: linear-gradient(145deg, rgba(14,165,233,0.08), rgba(99,102,241,0.12));
            border: 1px solid rgba(99,102,241,0.35);
            border-radius: 14px;
            padding: 1rem 1rem;
            margin-bottom: 0.9rem;
            box-sizing: border-box;
            width: 100%;
            overflow-wrap: break-word;
            word-break: break-word;
        ">
            <div style="display:flex; flex-wrap:wrap; justify-content:space-between; align-items:flex-start; gap:4px; margin-bottom:0.4rem;">
                <span style="font-family:'Orbitron',sans-serif; font-size:0.78rem; color:#38BDF8; font-weight:700; flex-shrink:0; max-width:60%;">
                    👤 {fb.get('name','')}
                </span>
                <span style="font-size:0.7rem; color:#6366F1;">{fb.get('time','')}</span>
            </div>
            <div style="font-size:0.92rem; margin-bottom:0.5rem;">{fb.get('rating','')}</div>
            <div style="font-size:0.84rem; color:inherit; line-height:1.7; overflow-wrap:break-word; word-break:break-word; opacity:0.95;">"{fb.get('comment','')}"</div>
        </div>
        """, unsafe_allow_html=True)

st.divider()

#        PRESENTATION 
st.markdown('<div class="section-label">About SmartPrice AI</div>', unsafe_allow_html=True)

pdf_url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/final_smartpriceai.pdf"
viewer  = f"https://docs.google.com/viewer?url={pdf_url}&embedded=true"

st.markdown(f"""
<div style="position:relative;">
  <iframe src="{viewer}" width="100%" height="520px"
    style="border:1px solid rgba(56,189,248,0.3);border-radius:16px;display:block;"
    id="pdf-iframe">
  </iframe>
</div>
<div style="margin-top:0.6rem; text-align:center;">
  <a href="{viewer}" target="_blank"
     style="display:inline-block; padding:0.5rem 1.4rem;
            background:linear-gradient(135deg,#6366f1,#38bdf8);
            color:white; border-radius:10px; text-decoration:none;
            font-size:0.9rem; font-weight:600;">
    📄 Open SmartPrice AI pdf
  </a>
</div>
""", unsafe_allow_html=True)
st.divider()

st.caption("Built with Streamlit · Linear Regression · NEPSE Stock Data")
st.caption("2026 © Team Rudraksha")