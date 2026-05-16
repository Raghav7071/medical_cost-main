import streamlit as st

from core.auth_ui import render_auth_gate, render_logout, render_sidebar
from core.session import init_state
from core.styling import apply_css
from repositories.db import init_db
from ui.components import render_sidebar_nav
from ui.pages import (
    analytics,
    chatbot_page,
    dashboard,
    ocr_page,
    packages,
    prediction,
    recommendation,
    report_analysis,
    visa
)


st.set_page_config(page_title="MediGuide AI", page_icon="🏥", layout="wide", initial_sidebar_state="expanded")

init_db()
init_state()
apply_css()

if not st.session_state["user_id"]:
    render_auth_gate()
    st.stop()

render_sidebar()
render_sidebar_nav()
render_logout()

PAGES = {
    "dashboard": dashboard.render,
    "prediction": prediction.render,
    "analytics": analytics.render,
    "recommendation": recommendation.render,
    "ocr": ocr_page.render,
    "report_analysis": report_analysis.render,
    "visa": visa.render,
    "chatbot": chatbot_page.render,
    "packages": packages.render,
}

PAGES[st.session_state.page]()

