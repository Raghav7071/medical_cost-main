import streamlit as st

from repositories.db import db_size_kb
from repositories.predictions import get_admin_stats
from ui.components import leader_row, metric_card, page_title, rule


def render() -> None:
    page_title("Where things stand.", eyebrow="07 / OVERVIEW")
    st.markdown(
        "<p class='speako-sub'>Your runs, your saves, what the network looked like today.</p>",
        unsafe_allow_html=True,
    )

    stats = get_admin_stats()

    st.markdown(rule("LIVE METRICS"), unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(metric_card("PREDICTIONS RUN", f"{stats['total_predictions']:,}"), unsafe_allow_html=True)
    c2.markdown(metric_card("USERS", f"{stats['total_users']:,}"), unsafe_allow_html=True)
    c3.markdown(metric_card("TOP DISEASE", stats["top_disease"], value_size="20px"), unsafe_allow_html=True)
    c4.markdown(metric_card("DB SIZE", f"{db_size_kb():,.1f} KB"), unsafe_allow_html=True)

    st.markdown(rule("QUICK ACTIONS"), unsafe_allow_html=True)
    quick_actions = [
        ("01.", "ESTIMATE",
         "Tell the model what you need. It returns the median, the spread, and the per-line breakdown."),
        ("02.", "INTAKE",
         "Drop in a PDF, scan, or phone photo. The extractor pulls structured fields."),
        ("03.", "MATCH",
         "Rank partner hospitals by outcome data and price fit. No referral fees in the loop."),
    ]
    actions_html = "".join(
        f"<div class='manifesto-item'>"
        f"<div class='n'>{n}</div>"
        f"<div><div class='t'>{t}</div><p class='b'>{b}</p></div>"
        f"</div>"
        for n, t, b in quick_actions
    )
    st.markdown(actions_html, unsafe_allow_html=True)

    st.markdown(rule("RECENT ACTIVITY"), unsafe_allow_html=True)
    history = st.session_state.get("prediction_history", [])
    if history:
        lines = []
        for activity in reversed(history[-8:]):
            ts = activity.get("time", "--:--")
            kind = activity.get("type", "EVENT").upper().replace(" ", "_")
            detail = activity.get("details", "")
            lines.append(
                f"<span class='ts'>[{ts}]</span>  "
                f"{kind:<14}  {detail}"
            )
        log_html = "<br/>".join(lines)
        st.markdown(f"<div class='log-block'>{log_html}</div>", unsafe_allow_html=True)
    else:
        st.markdown(
            "<div class='log-block'>"
            "<span class='ts'>--:--</span>  no activity yet. run an estimate to see your log."
            "</div>",
            unsafe_allow_html=True,
        )
