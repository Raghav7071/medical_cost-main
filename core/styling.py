import streamlit as st

# ---------- design tokens ----------
# Calm healthcare aesthetic: white surfaces, soft blue/teal tints, muted navy text,
# gentle 12-14px radii, soft minimal shadows, Inter typography.

PAPER = "#F7FAFC"          # warm-off-white app background
INK = "#1E3A5F"            # muted navy for headings and body
SUBTEXT = "#5B7185"        # secondary text
SURFACE = "#FFFFFF"        # cards and panels
HAIRLINE = "#E4ECF3"       # borders and dividers
SIGNAL = "#3B82F6"         # softer medical blue (primary accent)
SIGNAL_DK = "#2563EB"      # hover-only; never a gradient stop
TINT_BLUE = "#EAF4FF"      # tinted surfaces / banners
TINT_TEAL = "#D7F0EA"      # secondary accent surfaces
TINT_WARM = "#FFF6E8"      # warm surface (doctor consultation)
SUCCESS = "#0F9D7A"        # availability dot / success messages
WARNING = "#D97706"
DANGER = "#DC2626"

# Back-compat aliases (pages still import these names).
PURPLE = SIGNAL
PURPLE_DARK = SIGNAL_DK
PURPLE_SOFT = TINT_BLUE
PURPLE_MID = "#93C5FD"
BORDER = HAIRLINE

# Soft shadow used everywhere — flat, no big drop shadows.
SOFT_SHADOW = "0 1px 2px rgba(30,58,95,0.04), 0 1px 1px rgba(30,58,95,0.03)"

_CSS = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    *, *::before, *::after {{
        box-sizing: border-box;
    }}

    html, body, .stApp, [class*="css"],
    .stMarkdown, .stText, button, input, textarea, select,
    [data-testid="stSidebar"], [data-testid="stHeader"],
    [data-testid="stMetric"], [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"], [data-testid="stChatMessage"],
    [data-testid="stMarkdownContainer"], [data-testid="stWidgetLabel"] {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;
    }}
    html, body, .stApp {{
        background: {PAPER};
        color: {INK};
        font-size: 15px;
        font-weight: 400;
        line-height: 1.6;
        -webkit-font-smoothing: antialiased;
    }}
    h1, h2, h3, h4, h5, h6 {{
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: -0.015em !important;
        color: {INK} !important;
    }}
    p, label, .stMarkdown, .stText {{
        color: {SUBTEXT};
    }}

    /* ---------- utility classes ---------- */

    .cap {{
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-size: 12px;
        font-weight: 600;
        color: {INK};
    }}
    .cap.sub {{ color: {SUBTEXT}; }}
    .cap.signal {{ color: {SIGNAL}; }}

    .signal {{ color: {SIGNAL} !important; }}

    .numeric {{
        font-weight: 700;
        font-size: 32px;
        line-height: 1.15;
        letter-spacing: -0.015em;
        color: {INK};
    }}
    .numeric.signal {{ color: {SIGNAL}; }}

    /* row with label / value */
    .leader {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 0;
        border-bottom: 1px solid {HAIRLINE};
        font-size: 14px;
    }}
    .leader:last-child {{ border-bottom: none; }}
    .leader .label {{ color: {SUBTEXT}; font-weight: 500; }}
    .leader .value {{ font-weight: 600; color: {INK}; }}
    .leader .value.signal {{ color: {SIGNAL}; }}
    .leader .dots {{ display: none; }}

    /* rule */
    .rule {{
        display: flex;
        align-items: center;
        gap: 16px;
        margin: 40px 0 24px 0;
    }}
    .rule .line {{ flex: 1; height: 1px; background: {HAIRLINE}; }}
    .rule .lbl {{
        font-size: 13px;
        font-weight: 600;
        color: {SUBTEXT};
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }}

    /* generic card */
    .hairline-card, .glass-card, .speako-card, .speako-feature {{
        background: {SURFACE};
        border: 1px solid {HAIRLINE};
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: {SOFT_SHADOW};
        transition: border-color 0.2s ease;
    }}
    .hairline-card:hover, .glass-card:hover {{
        border-color: #CED9E5;
    }}

    /* colophon footer */
    .colophon {{
        border-top: 1px solid {HAIRLINE};
        padding: 20px 0;
        margin-top: 24px;
        font-size: 13px;
        color: {SUBTEXT};
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 16px;
    }}
    .colophon-links a {{
        color: {SUBTEXT};
        text-decoration: none;
        margin-left: 16px;
        font-weight: 500;
    }}
    .colophon-links a:hover {{ color: {SIGNAL}; }}

    /* ---------- brand bar ---------- */
    .brand-bar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 16px 0;
        margin-bottom: 24px;
    }}
    .brand-bar .mark {{
        font-size: 18px;
        font-weight: 700;
        color: {INK};
        display: flex;
        align-items: center;
        gap: 8px;
    }}
    .brand-bar .meta {{
        font-size: 13px;
        color: {SUBTEXT};
        font-weight: 500;
        background: {SURFACE};
        padding: 4px 12px;
        border-radius: 20px;
        border: 1px solid {HAIRLINE};
    }}

    /* ---------- sticky site nav (landing) ---------- */
    .site-nav {{
        position: sticky;
        top: 0;
        z-index: 30;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
        padding: 12px 4px;
        margin: -1rem -4px 20px -4px;
        background: rgba(255,255,255,0.94);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border-bottom: 1px solid {HAIRLINE};
    }}
    .site-nav .brand {{
        font-size: 17px;
        font-weight: 700;
        color: {INK};
        display: flex;
        align-items: center;
        gap: 8px;
    }}
    .site-nav .brand .dot {{
        width: 22px; height: 22px;
        border-radius: 6px;
        background: {TINT_BLUE};
        color: {SIGNAL};
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 13px;
    }}
    .site-nav .links {{
        display: flex;
        gap: 22px;
        align-items: center;
    }}
    .site-nav .links a {{
        color: {INK};
        text-decoration: none;
        font-size: 14px;
        font-weight: 500;
        opacity: 0.78;
        transition: opacity 0.15s ease;
    }}
    .site-nav .links a:hover {{ opacity: 1; color: {SIGNAL}; }}
    .site-nav .links a:focus-visible {{
        outline: 2px solid {SIGNAL};
        outline-offset: 4px;
        border-radius: 4px;
        opacity: 1;
    }}
    .site-nav .signin {{
        font-size: 14px;
        font-weight: 600;
        color: {SIGNAL};
        background: {TINT_BLUE};
        border: 1px solid {HAIRLINE};
        padding: 8px 16px;
        border-radius: 8px;
        text-decoration: none;
    }}
    .site-nav .signin:hover {{ background: #DCEBFF; }}
    @media (max-width: 760px) {{
        .site-nav .links {{ display: none; }}
    }}

    /* ---------- buttons ---------- */
    .stButton>button, .stDownloadButton>button, .stFormSubmitButton>button {{
        background: {SIGNAL};
        color: #FFFFFF !important;
        border: 1px solid {SIGNAL};
        border-radius: 8px;
        font-weight: 600;
        font-size: 14px;
        padding: 11px 22px;
        min-height: 42px;
        width: 100%;
        transition: background 0.15s ease, border-color 0.15s ease;
        box-shadow: none;
    }}
    .stButton>button *, .stDownloadButton>button *, .stFormSubmitButton>button * {{
        color: #FFFFFF !important;
    }}
    .stButton>button:hover, .stDownloadButton>button:hover, .stFormSubmitButton>button:hover {{
        background: {SIGNAL_DK};
        border-color: {SIGNAL_DK};
    }}
    .stButton>button:focus-visible, .stDownloadButton>button:focus-visible {{
        outline: 3px solid rgba(59, 130, 246, 0.35);
        outline-offset: 2px;
    }}

    .btn-secondary>button {{
        background: {SURFACE} !important;
        color: {INK} !important;
        border: 1px solid {HAIRLINE} !important;
        box-shadow: none !important;
    }}
    .btn-secondary>button * {{ color: {INK} !important; }}
    .btn-secondary>button:hover {{
        background: {TINT_BLUE} !important;
        border-color: #C8D7E6 !important;
    }}

    /* ---------- inputs ---------- */
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stTextArea textarea,
    .stDateInput>div>div>input {{
        background: {SURFACE} !important;
        color: {INK} !important;
        border: 1px solid {HAIRLINE} !important;
        border-radius: 8px !important;
        font-size: 14px !important;
        padding: 11px 14px !important;
        box-shadow: none !important;
        transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
    }}
    .stTextInput>div>div>input:focus,
    .stNumberInput>div>div>input:focus,
    .stTextArea textarea:focus {{
        border-color: {SIGNAL} !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15) !important;
    }}

    /* Placeholder text — Streamlit's default is near-invisible against white.
       Use a muted slate that reads as "hint" without disappearing. */
    .stTextInput>div>div>input::placeholder,
    .stNumberInput>div>div>input::placeholder,
    .stTextArea textarea::placeholder,
    .stDateInput>div>div>input::placeholder,
    input[type="text"]::placeholder,
    input[type="password"]::placeholder,
    input[type="email"]::placeholder,
    input[type="number"]::placeholder,
    textarea::placeholder {{
        color: #94A3B8 !important;
        opacity: 1 !important;
        font-weight: 400 !important;
    }}
    /* Selectbox "Choose an option" placeholder (when no value selected) */
    .stSelectbox div[data-baseweb="select"] [class*="placeholder"],
    .stSelectbox div[data-baseweb="select"] [class*="Placeholder"] {{
        color: #94A3B8 !important;
        opacity: 1 !important;
    }}
    /* st.chat_input placeholder */
    [data-testid="stChatInput"] textarea::placeholder,
    [data-testid="stChatInputTextArea"]::placeholder {{
        color: #94A3B8 !important;
        opacity: 1 !important;
    }}
    .stSelectbox div[data-baseweb="select"] > div {{
        background: {SURFACE} !important;
        border: 1px solid {HAIRLINE} !important;
        border-radius: 8px !important;
        color: {INK} !important;
    }}
    /* The actual selected value lives in a nested span — Streamlit's default
       gives it low opacity so it reads as ghost text. Force full contrast. */
    .stSelectbox div[data-baseweb="select"] [data-baseweb="select-arrow"] svg {{
        color: {SUBTEXT} !important;
    }}
    .stSelectbox div[data-baseweb="select"] [aria-live="polite"],
    .stSelectbox div[data-baseweb="select"] [class*="ValueContainer"] *,
    .stSelectbox div[data-baseweb="select"] input,
    .stSelectbox div[data-baseweb="select"] span {{
        color: {INK} !important;
        opacity: 1 !important;
        font-size: 14px !important;
        font-weight: 500 !important;
    }}

    /* Dropdown popover (rendered in a portal at the body root, NOT inside
       .stSelectbox — that's why the parent rules above don't reach it). */
    div[data-baseweb="popover"],
    ul[role="listbox"],
    div[role="listbox"] {{
        background: {SURFACE} !important;
    }}
    div[data-baseweb="popover"] ul,
    ul[role="listbox"] {{
        background: {SURFACE} !important;
        border: 1px solid {HAIRLINE} !important;
        border-radius: 10px !important;
        box-shadow: {SOFT_SHADOW} !important;
        padding: 4px !important;
    }}
    div[data-baseweb="popover"] li,
    ul[role="listbox"] li,
    li[role="option"],
    div[role="option"] {{
        background: {SURFACE} !important;
        color: {INK} !important;
        font-size: 14px !important;
        padding: 9px 12px !important;
        border-radius: 6px !important;
    }}
    li[role="option"]:hover,
    div[role="option"]:hover,
    li[role="option"][aria-selected="true"],
    div[role="option"][aria-selected="true"] {{
        background: {TINT_BLUE} !important;
        color: {INK} !important;
    }}
    li[role="option"] *,
    div[role="option"] * {{
        color: {INK} !important;
    }}

    /* labels above inputs */
    .stTextInput label, .stNumberInput label, .stTextArea label,
    .stSelectbox label, .stDateInput label, .stFileUploader label,
    .stRadio label, .stCheckbox label {{
        font-size: 13px !important;
        font-weight: 600 !important;
        color: {INK} !important;
        margin-bottom: 6px !important;
    }}

    /* ---------- radio group ---------- */
    div[role="radiogroup"] {{
        background: #F1F5F9;
        border-radius: 8px;
        padding: 4px;
        display: inline-flex !important;
        gap: 2px;
    }}
    div[role="radiogroup"] label {{
        padding: 8px 16px !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        color: {SUBTEXT} !important;
        background: transparent;
        border-radius: 6px;
        cursor: pointer;
        transition: color 0.15s;
    }}
    div[role="radiogroup"] label:hover {{ color: {INK} !important; }}
    div[role="radiogroup"] label[data-baseweb="radio"]:has(input:checked) {{
        background: {SURFACE} !important;
        color: {INK} !important;
        box-shadow: {SOFT_SHADOW};
        font-weight: 600 !important;
    }}

    /* ---------- sidebar ---------- */
    [data-testid="stSidebar"] {{
        background: {SURFACE};
        border-right: 1px solid {HAIRLINE};
    }}
    [data-testid="stSidebar"] .stButton>button {{
        background: transparent;
        color: {SUBTEXT} !important;
        border: none;
        box-shadow: none;
        text-align: left;
        justify-content: flex-start;
        padding: 10px 16px;
        font-weight: 500;
        font-size: 14px;
        border-radius: 8px;
        margin-bottom: 4px;
        min-height: 38px;
    }}
    [data-testid="stSidebar"] .stButton>button * {{ color: {SUBTEXT} !important; }}
    [data-testid="stSidebar"] .stButton>button:hover {{
        background: {TINT_BLUE};
        color: {INK} !important;
    }}
    [data-testid="stSidebar"] .stButton>button:hover * {{ color: {INK} !important; }}
    [data-testid="stSidebar"] .stButton>button.active {{
        background: {TINT_BLUE};
        color: {SIGNAL} !important;
        font-weight: 600;
    }}
    [data-testid="stSidebar"] .stButton>button.active * {{ color: {SIGNAL} !important; }}

    /* ---------- streamlit chrome cleanup ---------- */
    /* Hide Streamlit's top header bar (deploy/status indicator) entirely so the
       sticky site-nav sits flush at the top of the viewport. */
    header[data-testid="stHeader"] {{ display: none; }}
    [data-testid="stToolbar"] {{ display: none; }}
    [data-testid="stDecoration"] {{ display: none; }}
    .block-container {{ padding-top: 1rem; max-width: 1180px; }}

    /* Column rows: center-align children instead of stretching to equal height.
       Stretch caused short columns (e.g. copy next to a taller card) to grow
       and look broken. */
    [data-testid="stHorizontalBlock"] {{
        align-items: center;
    }}

    div[data-testid="stMetric"] {{
        background: {SURFACE};
        border: 1px solid {HAIRLINE};
        border-radius: 12px;
        padding: 20px;
        box-shadow: {SOFT_SHADOW};
    }}
    div[data-testid="stMetric"] label {{
        color: {SUBTEXT} !important;
        font-weight: 500 !important;
        font-size: 13px !important;
    }}
    div[data-testid="stMetricValue"] {{
        font-size: 30px !important;
        font-weight: 700 !important;
        color: {INK} !important;
    }}

    /* chat bubbles */
    [data-testid="stChatMessage"] {{
        background: {SURFACE};
        border: 1px solid {HAIRLINE};
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 12px;
        box-shadow: {SOFT_SHADOW};
    }}

    /* auth wrapper / card */
    .auth-wrapper {{ max-width: 440px; margin: 6vh auto 0 auto; }}
    .auth-card {{
        background: {SURFACE};
        border: 1px solid {HAIRLINE};
        border-radius: 14px;
        padding: 36px;
        box-shadow: {SOFT_SHADOW};
    }}

    /* badge */
    .speako-badge {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: {TINT_BLUE};
        color: {SIGNAL};
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }}
    .speako-badge.success {{
        background: {TINT_TEAL};
        color: {SUCCESS};
    }}
    .speako-badge .dot {{ width: 6px; height: 6px; border-radius: 50%; background: currentColor; }}

    /* ---------- hero (landing) ---------- */
    .hero-title {{
        font-size: 44px;
        font-weight: 700;
        line-height: 1.12;
        letter-spacing: -0.015em;
        color: {INK};
        margin: 0 0 18px 0;
    }}
    .hero-subtitle {{
        font-size: 17px;
        line-height: 1.65;
        color: {SUBTEXT};
        margin-bottom: 28px;
        max-width: 540px;
    }}
    .hero-eyebrow {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: {TINT_TEAL};
        color: {SUCCESS};
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.02em;
        margin-bottom: 20px;
    }}
    .hero-eyebrow .dot {{
        width: 6px; height: 6px; border-radius: 50%; background: currentColor;
    }}
    .hero-illus {{
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 12px;
    }}

    /* hero CTA pair (anchors styled as buttons so href works natively) */
    .hero-ctas {{
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
        margin: 4px 0 8px 0;
    }}
    .hero-ctas .cta {{
        flex: 0 0 220px;        /* equal-width, regardless of label length */
        height: 46px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 0 18px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 14.5px;
        text-decoration: none;
        transition: background 0.15s ease, border-color 0.15s ease, color 0.15s ease;
        border: 1px solid transparent;
        white-space: nowrap;
    }}
    .hero-ctas .cta.primary {{
        background: {SIGNAL};
        color: #FFFFFF !important;
        border-color: {SIGNAL};
    }}
    .hero-ctas .cta.primary:hover {{
        background: {SIGNAL_DK};
        border-color: {SIGNAL_DK};
    }}
    .hero-ctas .cta.secondary {{
        background: {SIGNAL};
        color: #FFFFFF !important;
        border-color: {SIGNAL};
    }}
    .hero-ctas .cta.secondary:hover {{
        background: {SIGNAL_DK};
        border-color: {SIGNAL_DK};
    }}
    .hero-ctas .cta:focus-visible {{
        outline: 3px solid rgba(59, 130, 246, 0.35);
        outline-offset: 2px;
    }}
    @media (max-width: 520px) {{
        .hero-ctas .cta {{ flex: 1 1 100%; }}
    }}

    /* smooth-scroll for anchor links across the page */
    html {{ scroll-behavior: smooth; }}
    @media (max-width: 860px) {{
        .hero-title {{ font-size: 34px; }}
        .hero-subtitle {{ font-size: 16px; }}
    }}

    /* ---------- trust row ---------- */
    .trust-row {{
        display: flex;
        gap: 28px;
        margin-top: 36px;
        margin-bottom: 24px;
        flex-wrap: wrap;
        padding: 18px 0;
        border-top: 1px solid {HAIRLINE};
        border-bottom: 1px solid {HAIRLINE};
    }}
    .trust-item {{
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 13.5px;
        color: {SUBTEXT};
        font-weight: 500;
    }}
    .trust-item .check {{
        width: 18px; height: 18px;
        border-radius: 50%;
        background: {TINT_TEAL};
        color: {SUCCESS};
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 11px;
        font-weight: 700;
    }}

    /* ---------- section header ---------- */
    .section-eyebrow {{
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-size: 12px;
        font-weight: 600;
        color: {SIGNAL};
        margin-bottom: 8px;
    }}
    .section-title {{
        font-size: 30px;
        font-weight: 700;
        color: {INK};
        letter-spacing: -0.015em;
        margin: 0 0 10px 0;
    }}
    .section-kicker {{
        font-size: 16px;
        line-height: 1.6;
        color: {SUBTEXT};
        margin: 0 0 28px 0;
        max-width: 640px;
    }}

    /* ---------- stats grid ---------- */
    .stats-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 18px;
        margin: 28px 0;
    }}
    .stat-card {{
        background: {SURFACE};
        border: 1px solid {HAIRLINE};
        border-radius: 12px;
        padding: 22px;
        text-align: left;
        box-shadow: {SOFT_SHADOW};
    }}
    .stat-value {{
        font-size: 30px;
        font-weight: 700;
        color: {INK};
        margin-bottom: 6px;
        line-height: 1.1;
        letter-spacing: -0.015em;
    }}
    .stat-label {{
        font-size: 13.5px;
        color: {SUBTEXT};
        font-weight: 500;
    }}
    .stat-card .stat-value .accent {{ color: {SIGNAL}; }}

    /* ---------- medical guides grid ---------- */
    .guide-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 18px;
        margin: 8px 0 12px 0;
    }}
    @media (max-width: 980px) {{
        .guide-grid {{ grid-template-columns: repeat(2, 1fr); }}
    }}
    @media (max-width: 620px) {{
        .guide-grid {{ grid-template-columns: 1fr; }}
    }}
    .guide-card {{
        background: {SURFACE};
        border: 1px solid {HAIRLINE};
        border-radius: 12px;
        padding: 22px;
        box-shadow: {SOFT_SHADOW};
        transition: border-color 0.15s ease, box-shadow 0.15s ease, background 0.15s ease;
        display: block;
        text-decoration: none;
        color: inherit;
        cursor: pointer;
    }}
    .guide-card:hover {{
        border-color: {SIGNAL};
        background: #FBFDFF;
        box-shadow: 0 4px 12px rgba(30,58,95,0.06), 0 1px 2px rgba(30,58,95,0.04);
    }}
    .guide-card:hover .more {{
        text-decoration: underline;
    }}
    .guide-card:focus-visible {{
        outline: 3px solid rgba(59, 130, 246, 0.35);
        outline-offset: 2px;
    }}
    .guide-card .icon {{
        width: 42px; height: 42px;
        border-radius: 10px;
        background: {TINT_BLUE};
        color: {SIGNAL};
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 14px;
    }}
    .guide-card .icon.teal {{ background: {TINT_TEAL}; color: {SUCCESS}; }}
    .guide-card .icon.warm {{ background: {TINT_WARM}; color: {WARNING}; }}
    .guide-card h4 {{
        font-size: 16px;
        font-weight: 700;
        color: {INK};
        margin: 0 0 6px 0;
    }}
    .guide-card p {{
        font-size: 14px;
        line-height: 1.55;
        color: {SUBTEXT};
        margin: 0 0 12px 0;
    }}
    .guide-card .more {{
        font-size: 13px;
        font-weight: 600;
        color: {SIGNAL};
    }}

    /* ---------- symptoms checker preview ---------- */
    .symptom-preview {{
        background: {TINT_BLUE};
        border: 1px solid {HAIRLINE};
        border-radius: 14px;
        padding: 32px;
        margin: 8px 0;
    }}
    .symptom-card {{
        background: {SURFACE};
        border: 1px solid {HAIRLINE};
        border-radius: 12px;
        padding: 22px;
        box-shadow: {SOFT_SHADOW};
    }}
    .symptom-card .row {{
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 0;
        border-bottom: 1px solid {HAIRLINE};
        font-size: 14px;
        color: {INK};
    }}
    .symptom-card .row:last-child {{ border-bottom: none; }}
    .symptom-card .row .chk {{
        width: 18px; height: 18px;
        border-radius: 4px;
        border: 1.5px solid {HAIRLINE};
        background: {SURFACE};
        display: inline-flex; align-items: center; justify-content: center;
        font-size: 11px;
        color: {SUCCESS};
        font-weight: 700;
    }}
    .symptom-card .row .chk.on {{
        background: {TINT_TEAL};
        border-color: {SUCCESS};
    }}
    .symptom-card .meta {{
        font-size: 12px;
        color: {SUBTEXT};
        margin-top: 12px;
    }}
    .symptom-copy ul {{
        list-style: none;
        padding: 0;
        margin: 16px 0;
    }}
    .symptom-copy li {{
        padding: 6px 0;
        color: {SUBTEXT};
        font-size: 14.5px;
    }}
    .symptom-copy li::before {{
        content: "—";
        margin-right: 10px;
        color: {SIGNAL};
        font-weight: 700;
    }}

    /* ---------- voice card (health assistant) ---------- */
    .voice-card {{
        background: {SURFACE};
        border: 1px solid {HAIRLINE};
        border-radius: 14px;
        padding: 20px 22px;
        margin-bottom: 18px;
        box-shadow: {SOFT_SHADOW};
    }}
    .voice-card .head {{
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 4px;
    }}
    .voice-card .avatar {{
        width: 32px; height: 32px;
        border-radius: 50%;
        background: {TINT_BLUE};
        color: {SIGNAL};
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 14px;
        flex-shrink: 0;
    }}
    .voice-card .name {{
        font-weight: 700;
        font-size: 15px;
        color: {INK};
    }}
    .voice-card .tagline {{
        font-size: 13.5px;
        color: {SUBTEXT};
        margin: 0 0 10px 42px;
    }}
    .voice-status {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        font-size: 12.5px;
        color: {SUBTEXT};
        margin-top: 6px;
    }}
    .voice-status .dot {{
        width: 8px; height: 8px;
        border-radius: 50%;
        background: {SUCCESS};
    }}
    .voice-status.idle .dot {{ background: {SUCCESS}; }}
    .voice-status.busy .dot {{
        background: {SIGNAL};
        animation: pulse 1.2s ease-in-out infinite;
    }}
    @keyframes pulse {{
        0%, 100% {{ opacity: 0.4; transform: scale(0.85); }}
        50%      {{ opacity: 1;   transform: scale(1.15); }}
    }}

    /* chat bubbles for the assistant transcript */
    .chat-bubble {{
        max-width: 80%;
        padding: 12px 16px;
        border-radius: 14px;
        font-size: 14.5px;
        line-height: 1.55;
        margin-bottom: 10px;
        word-wrap: break-word;
    }}
    .chat-bubble.user {{
        background: {TINT_BLUE};
        color: {INK};
        margin-left: auto;
        border-bottom-right-radius: 4px;
    }}
    .chat-bubble.assistant {{
        background: {SURFACE};
        color: {INK};
        border: 1px solid {HAIRLINE};
        border-bottom-left-radius: 4px;
    }}
    .chat-row {{
        display: flex;
        margin-bottom: 4px;
    }}
    .chat-row.user {{ justify-content: flex-end; }}

    /* ---------- article cards ---------- */
    .article-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
        margin: 8px 0;
    }}
    @media (max-width: 860px) {{
        .article-grid {{ grid-template-columns: 1fr; }}
    }}
    .article-card {{
        background: {SURFACE};
        border: 1px solid {HAIRLINE};
        border-radius: 12px;
        overflow: hidden;
        box-shadow: {SOFT_SHADOW};
        display: flex;
        flex-direction: column;
        text-decoration: none;
        color: inherit;
        cursor: pointer;
        transition: border-color 0.15s ease, box-shadow 0.15s ease, background 0.15s ease;
    }}
    .article-card:hover {{
        border-color: {SIGNAL};
        background: #FBFDFF;
        box-shadow: 0 4px 12px rgba(30,58,95,0.06), 0 1px 2px rgba(30,58,95,0.04);
    }}
    .article-card:hover .read {{
        color: {SIGNAL};
    }}
    .article-card:focus-visible {{
        outline: 3px solid rgba(59, 130, 246, 0.35);
        outline-offset: 2px;
    }}
    .article-card .thumb {{
        height: 140px;
        background: linear-gradient(135deg, {TINT_BLUE} 0%, {TINT_TEAL} 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: {SIGNAL};
    }}
    .article-card .body {{ padding: 18px 20px 20px 20px; }}
    .article-card .tag {{
        display: inline-block;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: {SIGNAL};
        background: {TINT_BLUE};
        padding: 4px 10px;
        border-radius: 20px;
        margin-bottom: 10px;
    }}
    .article-card h4 {{
        font-size: 16px;
        font-weight: 700;
        color: {INK};
        margin: 0 0 6px 0;
        line-height: 1.35;
    }}
    .article-card p {{
        font-size: 14px;
        color: {SUBTEXT};
        line-height: 1.55;
        margin: 0 0 14px 0;
    }}
    .article-card .read {{
        font-size: 12.5px;
        color: {SUBTEXT};
        font-weight: 500;
    }}

    /* ---------- doctor cards ---------- */
    .doctor-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 18px;
        margin: 8px 0;
    }}
    @media (max-width: 860px) {{
        .doctor-grid {{ grid-template-columns: 1fr; }}
    }}
    .doctor-card {{
        background: {SURFACE};
        border: 1px solid {HAIRLINE};
        border-radius: 12px;
        padding: 20px;
        box-shadow: {SOFT_SHADOW};
        display: flex;
        gap: 16px;
        align-items: center;
        text-decoration: none;
        color: inherit;
        cursor: pointer;
        position: relative;
        transition: border-color 0.15s ease, box-shadow 0.15s ease, background 0.15s ease;
    }}
    .doctor-card:hover {{
        border-color: {SIGNAL};
        background: #FBFDFF;
        box-shadow: 0 4px 12px rgba(30,58,95,0.06), 0 1px 2px rgba(30,58,95,0.04);
    }}
    .doctor-card:focus-visible {{
        outline: 3px solid rgba(59, 130, 246, 0.35);
        outline-offset: 2px;
    }}
    .doctor-card .book-cue {{
        position: absolute;
        right: 18px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 13px;
        font-weight: 600;
        color: {SIGNAL};
        opacity: 0;
        transition: opacity 0.15s ease, transform 0.15s ease;
    }}
    .doctor-card:hover .book-cue {{
        opacity: 1;
        transform: translateY(-50%) translateX(2px);
    }}
    .doctor-card .avatar {{
        width: 52px; height: 52px;
        border-radius: 50%;
        background: {TINT_TEAL};
        color: {SUCCESS};
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 16px;
        flex-shrink: 0;
    }}
    .doctor-card .info {{ flex: 1; }}
    .doctor-card .name {{
        font-size: 15px;
        font-weight: 700;
        color: {INK};
        margin: 0 0 2px 0;
    }}
    .doctor-card .spec {{
        font-size: 13px;
        color: {SUBTEXT};
        margin: 0 0 8px 0;
    }}
    .doctor-card .status {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 12px;
        font-weight: 600;
        color: {SUCCESS};
    }}
    .doctor-card .status .dot {{
        width: 7px; height: 7px; border-radius: 50%; background: {SUCCESS};
    }}
    .doctor-card .status.away {{ color: {SUBTEXT}; }}
    .doctor-card .status.away .dot {{ background: {SUBTEXT}; }}

    /* ---------- testimonials ---------- */
    .testimonial-wrap {{
        background: {TINT_TEAL};
        border-radius: 14px;
        padding: 36px 28px;
        margin: 8px 0;
    }}
    .testimonial-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 18px;
    }}
    @media (max-width: 860px) {{
        .testimonial-grid {{ grid-template-columns: 1fr; }}
    }}
    .testimonial-card {{
        background: {SURFACE};
        border: 1px solid rgba(15, 157, 122, 0.18);
        border-radius: 12px;
        padding: 22px;
    }}
    .testimonial-card .quote {{
        font-size: 14.5px;
        color: {INK};
        line-height: 1.6;
        margin: 0 0 16px 0;
    }}
    .testimonial-card .quote::before {{
        content: "“";
        font-size: 26px;
        color: {SUCCESS};
        line-height: 0.6;
        margin-right: 2px;
        vertical-align: -0.1em;
    }}
    .testimonial-card .who {{
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    .testimonial-card .who .avatar {{
        width: 32px; height: 32px;
        border-radius: 50%;
        background: {TINT_BLUE};
        color: {SIGNAL};
        font-size: 12px; font-weight: 700;
        display: flex; align-items: center; justify-content: center;
    }}
    .testimonial-card .who .name {{
        font-size: 13px; font-weight: 600; color: {INK};
    }}
    .testimonial-card .who .role {{
        font-size: 12px; color: {SUBTEXT};
    }}

    /* ---------- steps ---------- */
    .steps-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
        gap: 18px;
        margin: 8px 0;
    }}
    .step-card {{
        background: {SURFACE};
        border: 1px solid {HAIRLINE};
        border-radius: 12px;
        padding: 24px;
        box-shadow: {SOFT_SHADOW};
    }}
    .step-icon-wrapper {{
        width: 44px;
        height: 44px;
        background: {TINT_BLUE};
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 0 16px 0;
        color: {SIGNAL};
    }}
    .step-title {{
        font-size: 16px;
        font-weight: 700;
        color: {INK};
        margin-bottom: 8px;
    }}
    .step-desc {{
        font-size: 14px;
        color: {SUBTEXT};
        line-height: 1.55;
    }}

    /* ---------- faq ---------- */
    .faq-item {{
        background: {SURFACE};
        border: 1px solid {HAIRLINE};
        border-radius: 12px;
        padding: 20px 22px;
        margin-bottom: 12px;
    }}
    .faq-q {{
        font-size: 15px;
        font-weight: 600;
        color: {INK};
        margin-bottom: 8px;
    }}
    .faq-a {{
        font-size: 14px;
        color: {SUBTEXT};
        line-height: 1.6;
        margin: 0;
    }}

    /* ---------- cta banner (flat, no gradient) ---------- */
    .cta-banner {{
        background: {TINT_BLUE};
        border: 1px solid {HAIRLINE};
        border-radius: 14px;
        padding: 40px 32px;
        text-align: center;
        color: {INK};
        margin: 24px 0;
    }}
    .cta-banner h2 {{
        color: {INK} !important;
        font-size: 26px;
        font-weight: 700;
        margin: 0 0 10px 0;
    }}
    .cta-banner p {{
        color: {SUBTEXT};
        font-size: 15.5px;
        max-width: 560px;
        margin: 0 auto 22px auto;
    }}

    /* ---------- footer grid ---------- */
    .footer-grid {{
        display: grid;
        grid-template-columns: 1.4fr 1fr 1fr 1fr;
        gap: 40px;
        padding: 40px 0 24px 0;
        margin-top: 40px;
        border-top: 1px solid {HAIRLINE};
    }}
    @media (max-width: 860px) {{
        .footer-grid {{ grid-template-columns: 1fr 1fr; gap: 28px; }}
    }}
    .footer-grid h5 {{
        font-size: 13px;
        font-weight: 700;
        color: {INK};
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin: 0 0 14px 0;
    }}
    .footer-grid ul {{
        list-style: none;
        padding: 0;
        margin: 0;
    }}
    .footer-grid li {{
        padding: 4px 0;
        font-size: 13.5px;
    }}
    .footer-grid a {{
        color: {SUBTEXT};
        text-decoration: none;
    }}
    .footer-grid a:hover {{ color: {SIGNAL}; }}
    .footer-grid .brand-col p {{
        font-size: 13.5px;
        color: {SUBTEXT};
        line-height: 1.6;
        max-width: 280px;
        margin: 8px 0 0 0;
    }}
    .footer-bottom {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 18px 0 28px 0;
        border-top: 1px solid {HAIRLINE};
        font-size: 12.5px;
        color: {SUBTEXT};
        flex-wrap: wrap;
        gap: 12px;
    }}
    .footer-bottom .legal a {{
        color: {SUBTEXT};
        text-decoration: none;
        margin-left: 18px;
    }}
    .footer-bottom .legal a:hover {{ color: {SIGNAL}; }}

    /* ---------- report / analysis cards (no glassmorphism) ---------- */
    .glass-report {{
        background: {SURFACE};
        border: 1px solid {HAIRLINE};
        border-radius: 12px;
        padding: 26px;
        margin-bottom: 18px;
        box-shadow: {SOFT_SHADOW};
    }}

    /* health-score circle */
    .health-score {{
        width: 112px;
        height: 112px;
        border-radius: 50%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: 0 auto;
        box-shadow: {SOFT_SHADOW};
    }}
    .health-score .value {{ font-size: 32px; font-weight: 700; line-height: 1; }}
    .health-score .label {{
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-top: 4px;
    }}

    /* flat progress bar (no gradient) */
    .grad-progress {{
        width: 100%;
        height: 8px;
        background: {HAIRLINE};
        border-radius: 8px;
        overflow: hidden;
    }}
    .grad-progress .fill {{
        height: 100%;
        border-radius: 8px;
        background: {SIGNAL};
        transition: width 0.4s ease;
    }}

    /* skeleton loading pulse */
    @keyframes skeletonPulse {{
        0%   {{ opacity: 0.6; }}
        50%  {{ opacity: 1; }}
        100% {{ opacity: 0.6; }}
    }}
    .skeleton {{
        background: linear-gradient(90deg, #F1F5F9 25%, #E4ECF3 50%, #F1F5F9 75%);
        background-size: 200% 100%;
        animation: skeletonPulse 1.5s ease-in-out infinite;
        border-radius: 8px;
    }}

    /* country selector cards */
    .country-card {{
        background: {SURFACE};
        border: 1px solid {HAIRLINE};
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        cursor: pointer;
        transition: border-color 0.15s ease, background 0.15s ease;
    }}
    .country-card:hover {{
        border-color: #C8D7E6;
        background: {TINT_BLUE};
    }}
    .country-card.active {{
        border: 1.5px solid {SIGNAL};
        background: {TINT_BLUE};
    }}

    /* file uploader */
    .stFileUploader section {{
        border: 1.5px dashed {HAIRLINE} !important;
        border-radius: 12px !important;
        background: {SURFACE} !important;
        padding: 28px !important;
        transition: border-color 0.15s ease;
    }}
    .stFileUploader section:hover {{
        border-color: #C8D7E6 !important;
    }}

    /* risk badges */
    .risk-low  {{ color: {SUCCESS}; background: {TINT_TEAL}; }}
    .risk-med  {{ color: {WARNING}; background: {TINT_WARM}; }}
    .risk-high {{ color: {DANGER};  background: #FEF2F2; }}
    .risk-badge {{
        display: inline-block;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
    }}

    /* expanders modern style */
    .streamlit-expanderHeader, details summary {{
        background: transparent !important;
        border: none !important;
        border-bottom: 1px solid {HAIRLINE} !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        padding: 14px 0 !important;
        color: {INK} !important;
    }}

    /* alerts */
    div[data-testid="stAlert"] {{
        border: 1px solid {HAIRLINE};
        border-radius: 12px;
        background: {SURFACE};
    }}

    /* log block */
    .log-block {{
        background: {SURFACE};
        border: 1px solid {HAIRLINE};
        border-radius: 12px;
        padding: 16px 20px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 12px;
        line-height: 1.8;
        white-space: pre-wrap;
        color: {INK};
    }}
    .log-block .ts {{ color: {SUBTEXT}; }}
    .log-block .hit {{ color: {SIGNAL}; }}

    /* manifest/feature back-compat */
    .manifesto-item {{
        display: grid;
        grid-template-columns: 60px 1fr;
        gap: 20px;
        padding: 22px 0;
        border-top: 1px solid {HAIRLINE};
    }}
    .manifesto-item:last-child {{ border-bottom: 1px solid {HAIRLINE}; }}
    .manifesto-item .n {{ font-weight: 700; font-size: 14px; color: {SIGNAL}; }}
    .manifesto-item .t {{
        font-weight: 700; font-size: 16px; color: {INK}; margin: 0 0 6px 0;
    }}
    .manifesto-item .b {{
        color: {SUBTEXT}; font-size: 14px; line-height: 1.6; margin: 0;
    }}

    /* speako-stat back-compat */
    .speako-stats-wrapper {{
        background: {SURFACE};
        border: 1px solid {HAIRLINE};
        border-radius: 12px;
        display: grid;
        grid-template-columns: 1fr;
        margin: 18px 0 32px 0;
        overflow: hidden;
    }}
    .speako-stat {{
        padding: 16px 22px;
        border-bottom: 1px solid {HAIRLINE};
        display: flex;
        justify-content: space-between;
        align-items: baseline;
    }}
    .speako-stat:last-child {{ border-bottom: none; }}
    .speako-stat-value {{ font-size: 22px; font-weight: 700; color: {SIGNAL}; }}
    .speako-stat-label {{ color: {SUBTEXT}; font-size: 13px; font-weight: 500; }}

    /* metric card back-compat */
    .metric-title {{
        color: {SUBTEXT}; font-size: 13px; font-weight: 600; margin-bottom: 6px;
    }}
    .metric-value {{
        color: {INK};
        font-size: 30px;
        font-weight: 700;
        letter-spacing: -0.015em;
        line-height: 1.1;
    }}
    .title-text {{
        color: {INK}; font-weight: 700; letter-spacing: -0.015em;
    }}

    /* pill back-compat */
    .speako-pill {{
        display: inline-block;
        padding: 4px 12px;
        background: {TINT_BLUE};
        color: {SIGNAL};
        font-size: 12px;
        font-weight: 600;
        border-radius: 20px;
        margin-bottom: 12px;
    }}
    .speako-pill.gray {{ background: #F1F5F9; color: {SUBTEXT}; }}

    /* feature card back-compat */
    .speako-feature-title {{
        font-size: 16px; font-weight: 700; color: {INK}; margin-bottom: 6px;
    }}
    .speako-feature-body {{
        font-size: 14px; color: {SUBTEXT}; line-height: 1.6;
    }}

    /* speako-section back-compat */
    .speako-section {{ margin: 36px 0 14px 0; }}
    .speako-section h2 {{ font-size: 26px; margin: 6px 0 0 0; }}

    /* speako-purple-banner back-compat → flat tinted banner */
    .speako-purple-banner {{
        background: {TINT_BLUE};
        color: {INK} !important;
        border: 1px solid {HAIRLINE};
        border-radius: 14px;
        padding: 32px 28px;
        margin: 28px 0;
    }}
    .speako-purple-banner * {{ color: {INK} !important; }}
    .speako-purple-banner h2 {{
        color: {INK} !important;
        margin: 0 0 8px 0;
        font-size: 24px;
    }}

    .speako-footer {{
        background: transparent;
        border-top: 1px solid {HAIRLINE};
        padding: 24px 0;
        margin-top: 32px;
        color: {SUBTEXT};
    }}

    /* faq back-compat */
    .faq-row {{
        background: {SURFACE};
        border: 1px solid {HAIRLINE};
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 12px;
    }}
    .faq-row .q {{
        font-size: 15px; font-weight: 600; color: {INK}; margin: 0 0 6px 0;
    }}
    .faq-row .a {{
        color: {SUBTEXT}; font-size: 14px; line-height: 1.6; margin: 0;
    }}

    /* speako-nav back-compat */
    .speako-nav {{ display: none; }}
    .speako-brand {{ font-weight: 700; }}

</style>
"""


def apply_css() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)
