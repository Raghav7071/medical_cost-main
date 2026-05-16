import pandas as pd
import plotly.express as px
import streamlit as st

from config import DATASET_CSV
from ui.components import apply_transparent_theme, leader_row, page_title, rule


@st.cache_data
def _load_data() -> pd.DataFrame:
    try:
        return pd.read_csv(DATASET_CSV)
    except Exception:
        return pd.DataFrame()


def render() -> None:
    page_title("What the data is doing.", eyebrow="04 / SIGNALS")
    st.markdown(
        "<p class='speako-sub'>Cost trends, hospital distribution, country mix. "
        "Read it the way you'd read a chart in The Economist.</p>",
        unsafe_allow_html=True,
    )

    df = _load_data()
    if df.empty:
        st.error("No dataset available. Run `python train.py` first.")
        return

    avg_cost = df["Treatment_Cost"].mean()
    top_country = df["Country"].mode()[0]
    top_disease = df["Disease"].mode()[0]
    n_rows = len(df)

    st.markdown(rule("HEADLINE FIGURES"), unsafe_allow_html=True)
    st.markdown(
        "<div class='hairline-card' style='padding:8px 22px;'>"
        + leader_row("MEAN GLOBAL TREATMENT COST", f"${avg_cost:,.0f}")
        + leader_row("MOST FREQUENT DESTINATION", str(top_country))
        + leader_row("MOST REQUESTED PROCEDURE", str(top_disease), signal=True)
        + leader_row("SAMPLE SIZE", f"{n_rows:,} cases")
        + "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(rule("01 / PATIENT COUNT BY COUNTRY"), unsafe_allow_html=True)
    counts = df["Country"].value_counts().reset_index()
    counts.columns = ["Country", "count"]
    fig = px.bar(counts, x="Country", y="count", color="Country")
    fig.update_layout(showlegend=False)
    st.plotly_chart(apply_transparent_theme(fig), use_container_width=True)

    st.markdown(rule("02 / COST DISTRIBUTION BY DISEASE"), unsafe_allow_html=True)
    fig = px.box(df, x="Disease", y="Total_Cost", color="Disease")
    fig.update_layout(showlegend=False)
    st.plotly_chart(apply_transparent_theme(fig), use_container_width=True)

    st.markdown(rule("03 / STAY DAYS VS COST"), unsafe_allow_html=True)
    sample_df = df.sample(min(2000, len(df)), random_state=42)
    fig = px.scatter(
        sample_df,
        x="Stay_Days",
        y="Total_Cost",
        color="Hospital_Type",
        size="Treatment_Cost",
        hover_data=["Country"],
    )
    st.plotly_chart(apply_transparent_theme(fig), use_container_width=True)
