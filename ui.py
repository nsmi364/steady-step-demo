"""
Steady Step - look and feel (matches the Report 2 prototype screens)
Presentation only: no data processing happens in this file.
"""

import html

import streamlit as st

NAVY, GREEN, CREAM, INK, MUTED, ORANGE = "#252A47", "#2F9E7B", "#F8F5EE", "#1E2235", "#6B6F80", "#F2884B"

CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=DM+Mono:wght@400;500&family=Fraunces:opsz,wght@9..144,600&display=swap');

html, body, .stApp, .stMarkdown, button, input, textarea, select, label {{ font-family: 'DM Sans', sans-serif; }}
.stApp {{ background: {CREAM}; color: {INK}; }}
.block-container {{ max-width: 1150px; padding-top: 1rem; }}
[data-testid="stToolbar"], [data-testid="stDecoration"] {{ display: none; }}
header[data-testid="stHeader"] {{ background: transparent; }}

/* ---------- sidebar ---------- */
section[data-testid="stSidebar"] {{ background: {NAVY}; }}
section[data-testid="stSidebar"] * {{ color: #D9DBE7; }}
section[data-testid="stSidebar"] [role="radiogroup"] label {{
  padding: 10px 12px; border-radius: 10px; margin: 2px 0; width: 100%; cursor: pointer; }}
section[data-testid="stSidebar"] [role="radiogroup"] label:hover {{ background: rgba(255,255,255,.06); }}
section[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {{
  background: rgba(255,255,255,.10); box-shadow: inset 3px 0 0 {GREEN}; }}
section[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) p {{ color: #fff; font-weight: 600; }}
section[data-testid="stSidebar"] .st-key-nav [data-baseweb="radio"] > div:first-child,
section[data-testid="stSidebar"] .st-key-nav [data-testid="stRadioOption"] > div > div:first-child {{ display: none; }}
section[data-testid="stSidebar"] .st-key-nav [data-testid="stRadio"],
section[data-testid="stSidebar"] .st-key-nav [role="radiogroup"] {{ width:100%; }}
section[data-testid="stSidebar"] .st-key-nav [role="radiogroup"] label {{ display:flex; width:100%; box-sizing:border-box; }}
section[data-testid="stSidebar"] .st-key-nav [role="radiogroup"] p {{ font-size:1rem; }}
section[data-testid="stSidebar"] [data-baseweb="select"] > div {{
  background: rgba(255,255,255,.08) !important; border-color: rgba(255,255,255,.2) !important; }}
section[data-testid="stSidebar"] [data-testid="stSelectbox"] [role="group"] {{
  background: rgba(255,255,255,.08) !important; border-color: rgba(255,255,255,.2) !important; }}
section[data-testid="stSidebar"] [data-testid="stSelectbox"] input,
section[data-testid="stSidebar"] [data-testid="stSelectbox"] svg,
section[data-testid="stSidebar"] [data-baseweb="select"] * {{ color:#fff !important; -webkit-text-fill-color:#fff !important; }}
.ss-logo {{ display:flex; align-items:center; gap:10px; font-weight:700; font-size:1.35rem; color:#fff !important; margin:4px 0 18px; }}
.ss-logo span.box {{ width:34px; height:34px; border-radius:9px; background:{GREEN}; display:inline-flex;
  align-items:center; justify-content:center; box-shadow: 3px 3px 0 {ORANGE}; color:#fff !important; font-size:1rem; }}
.ss-logo b {{ color: {GREEN} !important; }}
.ss-side-label {{ font-family:'DM Mono',monospace; font-size:.7rem; letter-spacing:.14em; color:#8B8FA8 !important; margin: 6px 0 2px; }}
.ss-side-card {{ background: rgba(255,255,255,.06); border:1px solid rgba(255,255,255,.08); border-radius:14px; padding:14px; margin-top:28px; }}
.ss-side-card b {{ color:#fff !important; }}

/* ---------- main ---------- */
.ss-crumb {{ font-family:'DM Mono',monospace; font-size:.75rem; letter-spacing:.12em; color:{MUTED}; padding-top:10px; }}
.ss-crumb .dot {{ color:{GREEN}; }}
.ss-eyebrow {{ font-family:'DM Mono',monospace; font-size:.75rem; letter-spacing:.16em; color:{GREEN}; text-transform:uppercase; margin-top:6px; }}
.ss-title {{ font-size:3rem; font-weight:700; line-height:1.08; letter-spacing:-.03em; color:{INK}; margin:6px 0 10px; }}
.ss-title em {{ font-family:'Fraunces',serif; font-style:normal; color:{GREEN}; letter-spacing:-.02em; }}
.ss-sub {{ color:{MUTED}; font-size:1.02rem; max-width:620px; }}
.ss-h2 {{ font-size:1.45rem; font-weight:500; color:{INK}; margin:0 0 10px; }}

.ss-card {{ background:#FFFDF9; border:1px solid #ECE6DA; border-radius:18px; padding:20px 22px; margin-bottom:14px; }}
.ss-dark {{ background:{NAVY}; border-radius:18px; padding:22px 24px; color:#fff; margin-bottom:14px; }}
.ss-dark * {{ color:#fff; }}
.ss-big {{ font-family:'Fraunces',serif; font-size:3.6rem; line-height:1; }}
.ss-bar {{ height:5px; background:rgba(255,255,255,.15); border-radius:9px; margin:18px 0 8px; }}
.ss-bar > div {{ height:5px; background:{GREEN}; border-radius:9px; }}
.ss-bubble {{ float:right; width:84px; height:84px; border-radius:50%; background:{GREEN}; text-align:center;
  padding-top:16px; box-shadow:0 0 0 10px rgba(47,158,123,.18); }}
.ss-bubble b {{ font-family:'Fraunces',serif; font-size:1.6rem; display:block; line-height:1; }}
.ss-bubble small {{ font-family:'DM Mono',monospace; font-size:.6rem; }}
.ss-ring {{ width:86px; height:86px; border-radius:50%; display:inline-flex; align-items:center; justify-content:center; float:left; margin-right:18px; }}
.ss-ring div {{ width:68px; height:68px; border-radius:50%; background:#FFFDF9; text-align:center; padding-top:12px; }}
.ss-ring b {{ font-family:'Fraunces',serif; font-size:1.5rem; display:block; line-height:1.1; }}
.ss-ring small {{ font-family:'DM Mono',monospace; font-size:.55rem; color:{MUTED}; }}
.ss-pill {{ display:inline-block; font-family:'DM Mono',monospace; font-size:.7rem; letter-spacing:.06em;
  padding:4px 10px; border-radius:99px; font-weight:500; }}
.ss-stat {{ display:flex; gap:12px; align-items:center; padding:6px 0; }}
.ss-stat .ic {{ width:38px; height:38px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:1.1rem; }}
.ss-stat small {{ color:{MUTED}; display:block; font-size:.78rem; }}
.ss-stat b {{ font-family:'Fraunces',serif; font-size:1.45rem; }}
.ss-row {{ display:flex; justify-content:space-between; align-items:center; padding:12px 0; border-bottom:1px solid #EFEAE0; }}
.ss-row:last-child {{ border-bottom:none; }}
.ss-row small {{ color:{MUTED}; }}
.ss-date {{ width:56px; height:56px; border-radius:12px; background:#FDE7DA; text-align:center; padding-top:6px; float:left; margin-right:14px; }}
.ss-date b {{ font-family:'Fraunces',serif; font-size:1.5rem; display:block; line-height:1.05; }}
.ss-date small {{ font-family:'DM Mono',monospace; font-size:.6rem; }}
.ss-avatar {{ width:62px; height:62px; border-radius:50%; display:flex; align-items:center; justify-content:center;
  font-weight:700; font-family:'DM Mono',monospace; margin-bottom:14px; }}
.ss-chip {{ display:inline-block; background:#E3F4EC; color:#1F7A5C; border-radius:10px; padding:8px 14px; font-size:.9rem; margin:6px 0 12px; }}
.ss-quote {{ font-family:'Fraunces',serif; font-size:1.35rem; line-height:1.35; }}
.ss-mono {{ font-family:'DM Mono',monospace; font-size:.75rem; color:{MUTED}; }}
.ss-dashes span {{ display:inline-block; width:34px; height:5px; border-radius:9px; margin-left:6px; background:#E5E0D5; }}

/* buttons */
.stButton > button, .stFormSubmitButton > button {{ border-radius:10px; border:1px solid #E2DCCF; background:#FFFDF9; color:{INK}; font-weight:600; }}
.stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primary"] {{ background:{GREEN}; border-color:{GREEN}; color:#fff; }}
.stButton > button:hover {{ border-color:{GREEN}; color:{GREEN}; }}
.stButton > button[kind="primary"]:hover {{ color:#fff; filter:brightness(.95); }}
[class*="st-key-opt"] .stButton > button {{ height:110px; white-space:pre-line; }}
[data-testid="stMetric"] {{ background:#FFFDF9; border:1px solid #ECE6DA; border-radius:16px; padding:14px 18px; }}
</style>
"""

STATUS = {  # status -> (pill text, pill colours, ring colour, short message)
    "On track": ("ON TRACK", "#E3F4EC", "#1F7A5C", GREEN,
                 "You're showing up steadily. Keep the rhythm going."),
    "Worth keeping an eye on": ("WORTH A LOOK", "#FDEBDD", "#B5541B", ORANGE,
                                "You're close to your comfort zone. Small steps this week can help."),
    "Suggested check-in": ("LET'S CHAT", "#FBE3E3", "#B23A3A", "#E06666",
                           "A few things suggest a quick chat could help. That's support, not a penalty."),
}


def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)


def md(text):
    st.markdown(text, unsafe_allow_html=True)


def sidebar_logo():
    st.sidebar.markdown('<div class="ss-logo"><span class="box">▤</span><span>steadystep<b>.</b></span></div>',
                        unsafe_allow_html=True)


def side_label(text, where=None):
    (where or st.sidebar).markdown(f'<div class="ss-side-label">{text}</div>', unsafe_allow_html=True)


def side_card():
    st.sidebar.markdown('<div class="ss-side-card">✨<br><b>Small steps count.</b><br>'
                        '<small>One check-in at a time is enough.</small></div>', unsafe_allow_html=True)


def crumb(text):
    md(f'<div class="ss-crumb"><span class="dot">●</span> {text}</div>')


def heading(eyebrow, plain, green, sub=""):
    md(f'<div class="ss-eyebrow">{eyebrow}</div>'
       f'<div class="ss-title">{plain} <em>{green}</em></div>'
       + (f'<div class="ss-sub">{sub}</div>' if sub else ""))


def pill(status):
    text, bg, fg, _, _ = STATUS[status]
    return f'<span class="ss-pill" style="background:{bg};color:{fg}">● {text}</span>'


def ring(signals, status):
    colour = STATUS[status][3]
    deg = int(360 * max(signals, 0.08) / 3)
    return (f'<div class="ss-ring" style="background:conic-gradient({colour} {deg}deg,#EFEAE0 0)">'
            f'<div><b>{signals}/3</b><small>SIGNALS</small></div></div>')


def stat(icon, label, value, bg="#E3F4EC"):
    return (f'<div class="ss-stat"><div class="ic" style="background:{bg}">{icon}</div>'
            f'<div><small>{label}</small><b>{html.escape(str(value))}</b></div></div>')


def initials(name):
    return "".join(p[0] for p in name.split())[:2]
