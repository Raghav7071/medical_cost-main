import time
from datetime import datetime

import plotly.express as px
import streamlit as st

from ml.inference import load_pipelines, predict_costs
from repositories.predictions import save_prediction
from services.pdf_report import generate_pdf_report
from ui.components import (
    SIGNAL,
    apply_transparent_theme,
    leader_row,
    metric_card,
    page_title,
    rule,
)


# All cost outputs are displayed in USD — the base currency of the trained model.
CURRENCY_SYMBOL = "$"


def _collect_inputs(categories: dict) -> dict:
    col1, col2 = st.columns(2)
    with col1:
        disease = st.selectbox("DISEASE / CONDITION", categories["Disease"])
        country = st.selectbox("TARGET COUNTRY", categories["Country"])
        hospital_type = st.selectbox("HOSPITAL TYPE", categories["Hospital_Type"])
        doctor_exp = st.selectbox("DOCTOR EXPERIENCE", categories["Doctor_Experience"])
        insurance = st.selectbox("INSURANCE", categories["Insurance"])
    with col2:
        stay_days = st.number_input("STAY (DAYS)", 1, 365, 10)
        travel_class = st.selectbox("TRAVEL CLASS", categories["Travel_Class"])
        room_type = st.selectbox("ROOM CATEGORY", categories["Room_Type"])
        city = st.selectbox("TARGET CITY", categories["City"])

    return {
        "Disease": disease,
        "Country": country,
        "Hospital_Type": hospital_type,
        "Stay_Days": stay_days,
        "Travel_Class": travel_class,
        "Room_Type": room_type,
        "Doctor_Experience": doctor_exp,
        "Insurance": insurance,
        "City": city,
    }


def _render_breakdown(costs_in_target: dict[str, float], symbol: str) -> None:
    st.markdown(rule("BUDGET BREAKDOWN"), unsafe_allow_html=True)
    columns = st.columns(5)
    labels = [
        ("Treatment_Cost", "TREATMENT", None),
        ("Travel_Cost", "TRAVEL", None),
        ("Stay_Cost", "STAY", None),
        ("Medicine_Cost", "MEDICINE", None),
        ("Total_Cost", "TOTAL", SIGNAL),
    ]
    for col, (key, label, color) in zip(columns, labels):
        col.markdown(
            metric_card(label, f"{symbol}{costs_in_target[key]:,.0f}", color=color, value_size="22px"),
            unsafe_allow_html=True,
        )


def render() -> None:
    page_title("Tell us what you need. We'll tell you the number.", eyebrow="01 / ESTIMATE")
    st.markdown(
        "<p class='speako-sub'>The model is honest about uncertainty. The spread matters as much as the median.</p>",
        unsafe_allow_html=True,
    )

    models, categories, load_err = load_pipelines()
    if not models or not categories:
        st.error("ML models are missing. Run `python train.py` to generate them.")
        if load_err:
            st.caption(f"loader error: {load_err}")
        return

    st.markdown(rule("INPUTS"), unsafe_allow_html=True)
    with st.form("predict_form"):
        inputs = _collect_inputs(categories)
        submit = st.form_submit_button("RUN ESTIMATE →")

    if not submit:
        return

    with st.spinner("running pipeline..."):
        time.sleep(1)
        try:
            costs_in_target = predict_costs(models, inputs)
            symbol = CURRENCY_SYMBOL

            save_prediction(
                st.session_state["user_id"],
                inputs["Disease"],
                inputs["Country"],
                costs_in_target["Total_Cost"],
            )
            st.session_state["prediction_history"].append(
                {
                    "type": "Prediction",
                    "details": f"{inputs['Disease']} / {inputs['Country']} "
                    f"({symbol}{costs_in_target['Total_Cost']:,.0f})",
                    "time": datetime.now().strftime("%H:%M"),
                }
            )

            _render_breakdown(costs_in_target, symbol)

            st.markdown(rule("WHERE THE MONEY GOES"), unsafe_allow_html=True)
            fig = px.pie(
                values=[
                    costs_in_target["Treatment_Cost"],
                    costs_in_target["Travel_Cost"],
                    costs_in_target["Stay_Cost"],
                    costs_in_target["Medicine_Cost"],
                ],
                names=["TREATMENT", "TRAVEL", "STAY", "MEDICINE"],
                hole=0.55,
            )
            st.plotly_chart(apply_transparent_theme(fig), use_container_width=True)

            st.markdown(rule("EXPORT"), unsafe_allow_html=True)
            patient_details = {
                "Disease": inputs["Disease"],
                "Country": inputs["Country"],
                "Hospital": inputs["Hospital_Type"],
                "Stay": f"{inputs['Stay_Days']} Days",
            }
            cost_summary = {
                "Treatment": f"{symbol}{costs_in_target['Treatment_Cost']:,.2f}",
                "Travel": f"{symbol}{costs_in_target['Travel_Cost']:,.2f}",
                "Stay": f"{symbol}{costs_in_target['Stay_Cost']:,.2f}",
                "Medicine": f"{symbol}{costs_in_target['Medicine_Cost']:,.2f}",
                "Total Budget": f"{symbol}{costs_in_target['Total_Cost']:,.2f}",
            }
            pdf_path = generate_pdf_report(patient_details, cost_summary)
            with open(pdf_path, "rb") as pdf_file:
                st.download_button(
                    "EXPORT.pdf",
                    data=pdf_file,
                    file_name="MedTour_Estimate.pdf",
                    mime="application/pdf",
                )
        except Exception as e:
            st.error("Pipeline failed. See trace below.")
            st.caption(f"trace: {e}")
