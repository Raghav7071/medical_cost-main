import streamlit as st

from services.recommendation import compare_packages
from ui.components import (
    INK,
    SIGNAL,
    SUBTEXT,
    leader_row,
    page_title,
    rule,
)


_BASE_COST = 10000
_DISEASES = ["Heart Bypass", "Oncology", "Knee Replacement", "Cosmetic Surgery"]


def _tier_color(name: str) -> str:
    """Standard = ink (baseline), Premium = warm gray (one notch up), Luxury = signal red."""
    if name == "Premium":
        return SUBTEXT
    if name == "Luxury":
        return SIGNAL
    return INK


def render() -> None:
    if "current_package_page" not in st.session_state:
        st.session_state.current_package_page = "comparison"
    if "selected_package" not in st.session_state:
        st.session_state.selected_package = None

    if st.session_state.current_package_page == "comparison":
        _show_comparison()
    else:
        _show_package_details()


def _show_comparison() -> None:
    page_title("Three tiers. No upsells.", eyebrow="06 / PLANS")
    st.markdown(
        "<p class='speako-sub'>Pick one, see exactly what's included, book or move on.</p>",
        unsafe_allow_html=True,
    )

    st.markdown(rule("PROCEDURE"), unsafe_allow_html=True)
    disease = st.selectbox("SELECT TREATMENT", _DISEASES, key="compare_disease", label_visibility="collapsed")
    packages = compare_packages(disease)

    st.markdown(rule("TIERS"), unsafe_allow_html=True)
    cols = st.columns(3)
    for col, (name, details) in zip(cols, packages.items()):
        color = _tier_color(name)
        cost = _BASE_COST * details["Cost_Multiplier"]
        with col:
            st.markdown(
                f"<div class='hairline-card' style='padding:24px; border-top:3px solid {color};'>"
                f"<div class='cap' style='color:{color};'>{name.upper()}</div>"
                f"<div class='numeric' style='margin:10px 0 14px 0; font-size:38px; "
                f"color:{color};'>${cost:,.0f}</div>"
                + leader_row("ROOM", details["Room"])
                + leader_row("CONSULTS", str(details["Consultations"]))
                + leader_row("AIRPORT", details["Airport_Transfer"])
                + "</div>",
                unsafe_allow_html=True,
            )
            if st.button(f"SELECT {name.upper()} →", key=f"btn_{name}", use_container_width=True):
                st.session_state.selected_package = name
                st.session_state.current_package_page = "details"
                st.rerun()


def _benefits_for(name: str) -> list[str]:
    if name == "Standard":
        return [
            "Dedicated nursing staff",
            "Standard meals",
            "Post-op tele-consultation (1 week)",
        ]
    if name == "Premium":
        return [
            "24/7 dedicated nursing staff",
            "Personalized diet plan",
            "Fast-track visa assistance",
            "Post-op tele-consultation (1 month)",
        ]
    return [
        "24/7 private nursing staff",
        "Gourmet chef-prepared meals",
        "Premium visa processing",
        "Dedicated concierge",
        "Luxury wellness spa session",
        "Lifetime post-op tele-consultations",
    ]


def _show_package_details() -> None:
    name = st.session_state.selected_package
    disease = st.session_state.get("compare_disease", "Heart Bypass")
    packages = compare_packages(disease)

    if not name or name not in packages:
        st.session_state.current_package_page = "comparison"
        st.rerun()

    details = packages[name]
    cost = _BASE_COST * details["Cost_Multiplier"]
    color = _tier_color(name)

    col_back, col_title = st.columns([1.2, 5])
    with col_back:
        if st.button("← BACK", key="back_to_plans"):
            st.session_state.current_package_page = "comparison"
            st.rerun()
    with col_title:
        st.markdown(
            f"<div class='cap sub'>06 / PLANS · {name.upper()}</div>"
            f"<h2 style='font-size:30px; margin:6px 0 0 0; letter-spacing:-0.02em;'>"
            f"What's in {name.lower()}.</h2>",
            unsafe_allow_html=True,
        )

    st.markdown(rule("PROCEDURE"), unsafe_allow_html=True)

    benefits_html = "".join(
        f"<li style='margin:6px 0; list-style:none;'>"
        f"<span style='color:{SIGNAL}; margin-right:8px;'>+</span>{b}</li>"
        for b in _benefits_for(name)
    )

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(
            f"<div class='hairline-card' style='padding:24px; border-left:3px solid {color};'>"
            f"<div class='cap sub'>TREATMENT</div>"
            f"<h3 style='margin:4px 0 18px 0; font-size:18px; text-transform:uppercase; "
            f"letter-spacing:0.04em;'>{disease}</h3>"
            f"<div class='cap sub' style='margin-bottom:8px;'>INCLUSIONS</div>"
            + leader_row("ROOM TYPE", details["Room"])
            + leader_row("CONSULTATIONS", str(details["Consultations"]))
            + leader_row("AIRPORT TRANSFER", details["Airport_Transfer"])
            + f"<div class='cap sub' style='margin:18px 0 8px 0;'>ADDITIONAL BENEFITS</div>"
            + f"<ul style='padding-left:0; margin:0;'>{benefits_html}</ul>"
            + f"<div class='cap sub' style='margin:18px 0 8px 0;'>RECOVERY</div>"
            + f"<p style='margin:0;'>Average hospital stay of 7–14 days depending on patient health metrics.</p>"
            + "</div>",
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"<div class='hairline-card' style='padding:24px;'>"
            f"<div class='cap sub'>TOTAL PACKAGE</div>"
            f"<div class='numeric signal' style='font-size:42px; margin:6px 0 6px 0;'>${cost:,.0f}</div>"
            f"<p style='font-size:11px; color:{SUBTEXT}; text-transform:uppercase; "
            f"letter-spacing:0.06em; margin:0 0 16px 0;'>"
            f"Hospital fees, surgeon fees, facility charges.</p>"
            f"<div style='border-top:1px solid {INK}; margin:8px 0 12px 0;'></div>"
            f"</div>",
            unsafe_allow_html=True,
        )
        if st.button("BOOK APPOINTMENT →", type="primary", use_container_width=True):
            st.success(f"Booking requested for {name}. A coordinator will reach out.")

        st.markdown(
            "<div class='hairline-card' style='padding:18px; margin-top:14px;'>"
            "<div class='cap sub'>RECOMMENDED HOSPITAL</div>"
            "<h4 style='margin:6px 0; font-size:14px; text-transform:uppercase; "
            "letter-spacing:0.04em;'>Global Medical Center</h4>"
            + leader_row("RATING", "4.8 / 5.0")
            + leader_row("ACCREDITATION", "JCI", signal=True)
            + "</div>",
            unsafe_allow_html=True,
        )
