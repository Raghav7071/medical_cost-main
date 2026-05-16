"""Reusable Streamlit + Plotly building blocks. Soft healthcare aesthetic —
white surfaces, muted navy text, soft blue/teal tints, gentle radii, minimal
shadows. Pages still importing the older helpers continue to work; new landing
sections use the v2 card helpers below."""

from contextlib import contextmanager

import streamlit as st

from core.styling import (
    PAPER,
    INK,
    SIGNAL,
    SIGNAL_DK,
    SUBTEXT,
    SURFACE,
    HAIRLINE,
    TINT_BLUE,
    TINT_TEAL,
    TINT_WARM,
    SUCCESS,
)

# Back-compat: pages still import these names.
PURPLE = SIGNAL
PURPLE_DARK = SIGNAL_DK
PURPLE_SOFT = TINT_BLUE
PURPLE_MID = "#93C5FD"
BORDER = HAIRLINE

# Plotly palette — calm, distinguishable healthcare hues. Enough colors to
# avoid repetition on charts with up to ~12 categorical groups.
PLOTLY_PALETTE = [
    SIGNAL,      # medical blue
    "#7BB4F2",   # sky blue
    SUCCESS,     # calm green
    "#5EBFA8",   # teal
    "#F59E0B",   # warm amber
    "#E48A6B",   # dusty terracotta
    "#9C7BD1",   # soft violet
    "#3FB8C8",   # cyan
    "#D49EBA",   # dusty rose
    "#6B9B7F",   # sage
    "#C0A35E",   # ochre
    SUBTEXT,     # slate (fallback)
]


NAV_ITEMS = [
    ("Overview", "dashboard"),
    ("Estimate", "prediction"),
    ("Signals", "analytics"),
    ("Match", "recommendation"),
    ("Intake", "ocr"),
    ("Report Analysis", "report_analysis"),
    ("Medical Visa", "visa"),
    ("Health Assistant", "chatbot"),
    ("Care Plans", "packages"),
]


# ---------- cards ----------

@contextmanager
def glass_card(
    border_color: str | None = None,
    padding: str | None = None,
    border_top: str | None = None,
    text_align: str | None = None,
):
    """Hairline card context manager. Soft white surface with 1px hairline border
    and minimal shadow. Streamlit's div isolation means multi-child usage works,
    but for one-shot HTML it's still cleaner to build the card body as a single
    string and emit via st.markdown directly."""
    style_parts = [f"border:1px solid {HAIRLINE};"]
    if border_top:
        style_parts.append(f"border-top:3px solid {border_top};")
    if border_color:
        style_parts.append(f"border-left:3px solid {border_color};")
    style_parts.append(f"padding:{padding or '22px'};")
    if text_align:
        style_parts.append(f"text-align:{text_align};")
    style_parts.append(f"margin-bottom:16px;background:{SURFACE};border-radius:12px;")
    style = "".join(style_parts)
    st.markdown(f"<div class='hairline-card' style='{style}'>", unsafe_allow_html=True)
    try:
        yield
    finally:
        st.markdown("</div>", unsafe_allow_html=True)


def metric_card(title: str, value: str, color: str | None = None, value_size: str = "30px") -> str:
    """Hairline metric block. `color` (if given) becomes a left rule + value color."""
    border = f"border-left:3px solid {color};" if color else ""
    value_color = f"color:{color};" if color else ""
    return (
        f"<div class='hairline-card' style='{border} padding:18px;'>"
        f"<div class='metric-title'>{title}</div>"
        f"<div class='metric-value' style='font-size:{value_size}; {value_color}'>{value}</div>"
        f"</div>"
    )


# ---------- plotly theme ----------

def apply_transparent_theme(fig):
    """Plotly: transparent background, soft palette, Inter font."""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        colorway=PLOTLY_PALETTE,
        font=dict(family="Inter, sans-serif", color=INK, size=13),
        title_font=dict(family="Inter, sans-serif", color=INK, size=15),
        xaxis=dict(
            showgrid=False, zeroline=False, showline=True,
            linecolor=HAIRLINE, linewidth=1, ticks="outside", tickcolor=HAIRLINE,
            tickfont=dict(family="Inter, sans-serif", color=SUBTEXT, size=12),
        ),
        yaxis=dict(
            showgrid=True, gridcolor="#F1F5F9", zeroline=False, showline=False,
            ticks="outside", tickcolor="rgba(0,0,0,0)",
            tickfont=dict(family="Inter, sans-serif", color=SUBTEXT, size=12),
        ),
        margin=dict(l=40, r=20, t=40, b=40),
    )
    return fig


# ---------- page header ----------

def page_title(text: str, eyebrow: str | None = None) -> None:
    """Page header. `eyebrow` is the section code like '01 / ESTIMATE'."""
    eyebrow_html = (
        f"<div class='cap sub' style='margin-bottom:8px;'>{eyebrow}</div>"
        if eyebrow else ""
    )
    st.markdown(
        f"{eyebrow_html}"
        f"<h2 class='title-text' style='font-size:30px; margin:0 0 6px 0;'>{text}</h2>",
        unsafe_allow_html=True,
    )


def section_header_v2(eyebrow: str, title: str, kicker: str | None = None, anchor: str | None = None) -> str:
    """Section header for landing-page sections. Eyebrow + title + optional kicker.
    `anchor` (if given) becomes the section id, used for sticky-nav hash links."""
    kicker_html = f"<p class='section-kicker'>{kicker}</p>" if kicker else ""
    id_attr = f" id='{anchor}'" if anchor else ""
    return (
        f"<div{id_attr} style='margin: 56px 0 18px 0; scroll-margin-top: 80px;'>"
        f"<div class='section-eyebrow'>{eyebrow}</div>"
        f"<h2 class='section-title'>{title}</h2>"
        f"{kicker_html}"
        f"</div>"
    )


# ---------- pills / labels / rules ----------

def pill(text: str, variant: str = "default") -> str:
    cls = "speako-pill" if variant == "default" else "speako-pill gray"
    return f"<span class='{cls}'>{text}</span>"


def cap_label(text: str, variant: str = "default") -> str:
    cls = "cap" if variant == "default" else f"cap {variant}"
    return f"<div class='{cls}'>{text}</div>"


def leader_row(label: str, value: str, signal: bool = False) -> str:
    value_cls = "value signal" if signal else "value"
    return (
        f"<div class='leader'>"
        f"<span class='label'>{label}</span>"
        f"<span class='dots'></span>"
        f"<span class='{value_cls}'>{value}</span>"
        f"</div>"
    )


def rule(label: str | None = None) -> str:
    if label:
        return (
            f"<div class='rule'>"
            f"<div class='line'></div>"
            f"<div class='lbl'>{label}</div>"
            f"<div class='line'></div>"
            f"</div>"
        )
    return "<div class='rule'><div class='line'></div></div>"


def numeric(value: str, label: str, signal: bool = False) -> str:
    n_cls = "numeric signal" if signal else "numeric"
    return (
        f"<div>"
        f"<div class='cap sub'>{label}</div>"
        f"<div class='{n_cls}' style='margin-top:6px;'>{value}</div>"
        f"</div>"
    )


def section_header(eyebrow: str, title: str, center: bool = False) -> None:
    """Back-compat. New landing sections use `section_header_v2` instead."""
    st.markdown(
        f"<div class='cap sub' style='margin: 32px 0 6px 0;'>{eyebrow}</div>"
        f"<h2 style='font-size:26px; margin:0 0 16px 0; letter-spacing:-0.015em;'>{title}</h2>",
        unsafe_allow_html=True,
    )


def stat_block(value: str, label: str) -> str:
    return (
        f"<div class='speako-stat'>"
        f"<div class='speako-stat-label'>{label}</div>"
        f"<div class='speako-stat-value'>{value}</div>"
        f"</div>"
    )


def feature_card(icon_svg: str, title: str, body: str, tag: str | None = None) -> str:
    n = tag if tag else "—"
    return (
        f"<div class='manifesto-item'>"
        f"<div class='n'>{n}</div>"
        f"<div>"
        f"<div class='t'>{title}</div>"
        f"<p class='b'>{body}</p>"
        f"</div>"
        f"</div>"
    )


# ---------- landing v2 card helpers ----------

def guide_card(icon_svg: str, title: str, body: str, tone: str = "blue", href: str = "#") -> str:
    """Medical-guides category card: tinted icon chip + 2-line description.
    Wraps the card in an anchor so the whole tile is clickable."""
    icon_cls = "icon"
    if tone == "teal":
        icon_cls += " teal"
    elif tone == "warm":
        icon_cls += " warm"
    return (
        f"<a class='guide-card' href='{href}' target='_blank' rel='noopener noreferrer'>"
        f"<div class='{icon_cls}'>{icon_svg}</div>"
        f"<h4>{title}</h4>"
        f"<p>{body}</p>"
        f"<span class='more'>Learn more →</span>"
        f"</a>"
    )


def article_card(tag: str, title: str, excerpt: str, read_minutes: int, thumb_glyph: str = "", href: str = "#") -> str:
    """Health article preview. Wraps the whole tile in an anchor so it's clickable."""
    return (
        f"<a class='article-card' href='{href}' target='_blank' rel='noopener noreferrer'>"
        f"<div class='thumb'>{thumb_glyph}</div>"
        f"<div class='body'>"
        f"<span class='tag'>{tag}</span>"
        f"<h4>{title}</h4>"
        f"<p>{excerpt}</p>"
        f"<span class='read'>{read_minutes} min read · Read more →</span>"
        f"</div>"
        f"</a>"
    )


def doctor_card(initials: str, name: str, specialty: str, available: bool = True, href: str = "?auth=1") -> str:
    """Doctor consultation card: initials avatar + name + specialty + availability dot.
    Whole tile is a link — clicking prompts the auth flow so users can book."""
    status_cls = "status" if available else "status away"
    status_text = "Available today" if available else "Booking next week"
    return (
        f"<a class='doctor-card' href='{href}' target='_self'>"
        f"<div class='avatar'>{initials}</div>"
        f"<div class='info'>"
        f"<div class='name'>{name}</div>"
        f"<div class='spec'>{specialty}</div>"
        f"<span class='{status_cls}'><span class='dot'></span>{status_text}</span>"
        f"</div>"
        f"<span class='book-cue'>Book →</span>"
        f"</a>"
    )


def testimonial_card(quote: str, name: str, role: str, initials: str) -> str:
    """Patient testimonial: quote body + small avatar/name/role row."""
    return (
        f"<div class='testimonial-card'>"
        f"<p class='quote'>{quote}</p>"
        f"<div class='who'>"
        f"<div class='avatar'>{initials}</div>"
        f"<div>"
        f"<div class='name'>{name}</div>"
        f"<div class='role'>{role}</div>"
        f"</div>"
        f"</div>"
        f"</div>"
    )


# ---------- sidebar nav ----------

def render_sidebar_nav() -> None:
    with st.sidebar:
        st.markdown(
            "<div class='cap sub' style='margin: 14px 0 8px 0;'>NAVIGATE</div>",
            unsafe_allow_html=True,
        )
        for label, page in NAV_ITEMS:
            if st.button(label, key=f"nav_{page}"):
                st.session_state.page = page
                st.rerun()
