"""Inline SVG illustrations and glyphs. Soft healthcare aesthetic — monoline
1.5px strokes, two-tone accent (medical blue + soft teal), no animation. Older
modules import these names, so each is still exported."""

from __future__ import annotations

import streamlit as st

from core.styling import (
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

# Back-compat aliases.
PAPER = TINT_BLUE
PURPLE = SIGNAL
PURPLE_SOFT = TINT_BLUE


# Small brand mark used in the sticky nav and brand bar.
BRAND_MARK_SVG = (
    f'<svg width="28" height="28" viewBox="0 0 28 28" '
    f'xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
    f'<rect width="28" height="28" rx="7" fill="{TINT_BLUE}"/>'
    f'<path d="M14 7v14 M7 14h14" stroke="{SIGNAL}" stroke-width="2" stroke-linecap="round"/>'
    f'</svg>'
)


# Hand-crafted hero illustration. Stethoscope, clipboard with heart-rate trace,
# soft circle backdrop. Two-tone medical blue + soft teal. Flat structure (no
# <g> groups, no multi-line attribute values) so Streamlit's markdown pipeline
# can sanitize and render it without choking.
HERO_HEALTHCARE_SVG = (
    f'<svg width="480" height="360" viewBox="0 0 480 360" '
    f'xmlns="http://www.w3.org/2000/svg" aria-hidden="true" '
    f'style="max-width:100%; height:auto; display:block;">'
    f'<circle cx="295" cy="170" r="140" fill="{TINT_BLUE}"/>'
    f'<circle cx="130" cy="270" r="40" fill="{TINT_TEAL}" opacity="0.7"/>'
    f'<rect x="160" y="100" width="170" height="210" rx="10" fill="{SURFACE}" stroke="{SIGNAL}" stroke-width="2"/>'
    f'<rect x="208" y="86" width="74" height="26" rx="6" fill="{TINT_BLUE}" stroke="{SIGNAL}" stroke-width="2"/>'
    f'<line x1="180" y1="140" x2="290" y2="140" stroke="{HAIRLINE}" stroke-width="1.5" stroke-linecap="round"/>'
    f'<line x1="180" y1="160" x2="270" y2="160" stroke="{HAIRLINE}" stroke-width="1.5" stroke-linecap="round"/>'
    f'<path d="M178 220 L210 220 L222 200 L236 240 L252 210 L266 224 L312 224" fill="none" stroke="{SIGNAL}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
    f'<path d="M312 224 c -2 -6 -10 -6 -10 0 c 0 4 5 7 10 11 c 5 -4 10 -7 10 -11 c 0 -6 -8 -6 -10 0 Z" fill="{SUCCESS}"/>'
    f'<circle cx="184" cy="262" r="6" fill="{TINT_TEAL}" stroke="{SUCCESS}" stroke-width="1.5"/>'
    f'<path d="M181 262 l3 3 l5 -6" fill="none" stroke="{SUCCESS}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>'
    f'<line x1="200" y1="262" x2="290" y2="262" stroke="{HAIRLINE}" stroke-width="1.5" stroke-linecap="round"/>'
    f'<circle cx="184" cy="284" r="6" fill="{SURFACE}" stroke="{HAIRLINE}" stroke-width="1.5"/>'
    f'<line x1="200" y1="284" x2="270" y2="284" stroke="{HAIRLINE}" stroke-width="1.5" stroke-linecap="round"/>'
    f'<path d="M90 90 C 60 110, 50 160, 70 190 C 84 212, 110 218, 130 208" fill="none" stroke="{SIGNAL}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
    f'<path d="M90 90 C 120 110, 130 160, 110 190" fill="none" stroke="{SIGNAL}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
    f'<circle cx="90" cy="88" r="5" fill="{SIGNAL}"/>'
    f'<circle cx="110" cy="190" r="4.5" fill="{SIGNAL}"/>'
    f'<circle cx="135" cy="218" r="14" fill="{SURFACE}" stroke="{SIGNAL}" stroke-width="2.5"/>'
    f'<circle cx="135" cy="218" r="7" fill="{TINT_BLUE}" stroke="{SIGNAL_DK}" stroke-width="1.5"/>'
    f'<circle cx="370" cy="100" r="3" fill="{SIGNAL}" opacity="0.35"/>'
    f'<circle cx="400" cy="140" r="2" fill="{SIGNAL}" opacity="0.35"/>'
    f'<circle cx="380" cy="190" r="2.5" fill="{SIGNAL}" opacity="0.35"/>'
    f'</svg>'
)

# Decorative names kept for back-compat.
HERO_DOCTOR_SVG = HERO_HEALTHCARE_SVG
CTA_BANNER_SVG = ""


def _glyph(svg_inner: str, stroke: str | None = None) -> str:
    color = stroke or SIGNAL
    return (
        f'<svg width="22" height="22" viewBox="0 0 24 24" fill="none" '
        f'xmlns="http://www.w3.org/2000/svg" stroke="{color}" stroke-width="1.6" '
        f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{svg_inner}</svg>'
    )


# Soft monoline glyphs — 1.6px stroke, round caps, used for nav and feature cards.
FEATURE_PREDICT_SVG = _glyph(
    '<path d="M3 21 L9 13 L13 17 L21 5"/>'
    '<rect x="18.5" y="2.5" width="4" height="4" rx="0.6"/>'
)
FEATURE_HOSPITAL_SVG = _glyph(
    '<rect x="4" y="6" width="16" height="14" rx="1.5"/>'
    '<path d="M12 10v6 M9 13h6"/>'
)
FEATURE_OCR_SVG = _glyph(
    '<rect x="5" y="3" width="14" height="18" rx="1.5"/>'
    '<line x1="8" y1="9" x2="16" y2="9"/>'
    '<line x1="8" y1="13" x2="14" y2="13"/>'
    '<line x1="8" y1="17" x2="16" y2="17"/>'
)
FEATURE_CHAT_SVG = _glyph(
    '<path d="M4 5h16v12H9l-5 4V5z"/>'
)
FEATURE_PACKAGE_SVG = _glyph(
    '<path d="M12 3 L21 7 L21 17 L12 21 L3 17 L3 7 Z"/>'
    '<path d="M3 7 L12 11 L21 7 M12 11 V21"/>'
)
FEATURE_ANALYTICS_SVG = _glyph(
    '<rect x="4" y="13" width="3" height="7" rx="0.6"/>'
    '<rect x="10.5" y="8" width="3" height="12" rx="0.6"/>'
    '<rect x="17" y="4" width="3" height="16" rx="0.6"/>'
)
FEATURE_DASHBOARD_SVG = _glyph(
    '<rect x="3" y="3" width="8" height="8" rx="1.2"/>'
    '<rect x="13" y="3" width="8" height="5" rx="1.2"/>'
    '<rect x="3" y="13" width="8" height="8" rx="1.2"/>'
    '<rect x="13" y="10" width="8" height="11" rx="1.2"/>'
)


# Medical-guide category glyphs (24x24, 1.6px, round caps).
def category_glyph(name: str) -> str:
    name = name.lower()
    if name == "cardiology":
        return _glyph(
            '<path d="M12 21 C 5 16, 3 11, 5 8 C 7 5, 11 6, 12 9 '
            'C 13 6, 17 5, 19 8 C 21 11, 19 16, 12 21 Z"/>'
        )
    if name == "orthopedics":
        return _glyph(
            '<path d="M7 4 C 4 4, 4 7, 6 8 L 16 18 C 17 20, 20 20, 20 17 '
            'C 22 16, 22 13, 19 13 L 11 5 C 10 3, 7 3, 7 4 Z"/>'
        )
    if name == "maternal care":
        return _glyph(
            '<circle cx="12" cy="8" r="3"/>'
            '<path d="M6 21 C 6 16, 8 14, 12 14 C 16 14, 18 16, 18 21"/>'
            '<path d="M12 17 v3"/>'
        )
    if name == "pediatrics":
        return _glyph(
            '<circle cx="12" cy="9" r="4"/>'
            '<path d="M8.5 8 L 7 6 M15.5 8 L 17 6"/>'
            '<path d="M9 10 q 3 2 6 0"/>'
            '<path d="M5 21 C 5 16, 8 14, 12 14 C 16 14, 19 16, 19 21"/>'
        )
    if name == "mental health":
        return _glyph(
            '<path d="M8 5 a 4 4 0 0 0 -3 7 a 3 3 0 0 0 3 5 h 3 v 3"/>'
            '<path d="M11 17 v -3 h 2 a 3 3 0 0 0 3 -3 v -1 a 3 3 0 0 0 -3 -3"/>'
        )
    if name == "oncology":
        return _glyph(
            '<circle cx="12" cy="12" r="3"/>'
            '<path d="M12 4 v3 M12 17 v3 M4 12 h3 M17 12 h3 '
            'M6 6 l2 2 M16 16 l2 2 M6 18 l2 -2 M16 8 l2 -2"/>'
        )
    return _glyph('<circle cx="12" cy="12" r="6"/>')


def render_svg(svg: str, width: int | None = None) -> None:
    """Inject inline SVG via st.markdown. Skips empty strings cleanly."""
    if not svg:
        return
    style = f"width:{width}px;" if width else ""
    st.markdown(f"<div style='{style}'>{svg}</div>", unsafe_allow_html=True)
