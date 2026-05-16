import streamlit as st

from ml.inference import load_pipelines
from services.recommendation import get_doctors, get_hospitals
from ui.components import leader_row, page_title, rule


_DEFAULT_COUNTRIES = ["USA", "India", "Turkey", "Singapore", "Thailand", "Germany"]

# Hand-curated country→cities map. The dataset's `City` column is synthetic
# (same 7 cities for every country) so we can't derive a meaningful mapping
# from it. The recommendation engine only uses the city string for display
# templating, so values don't need to be in the ML model's category list.
_CITIES_BY_COUNTRY: dict[str, list[str]] = {
    "USA":       ["New York", "Los Angeles", "Houston", "Chicago", "Boston"],
    "India":     ["Mumbai", "Delhi", "Bangalore", "Chennai", "Hyderabad"],
    "Turkey":    ["Istanbul", "Ankara", "Izmir"],
    "Singapore": ["Singapore"],
    "Thailand":  ["Bangkok", "Phuket", "Chiang Mai"],
    "Germany":   ["Berlin", "Munich", "Hamburg", "Frankfurt"],
    "UK":        ["London", "Manchester", "Edinburgh", "Birmingham"],
    "UAE":       ["Dubai", "Abu Dhabi"],
    "France":    ["Paris", "Lyon", "Marseille"],
    "Canada":    ["Toronto", "Montreal", "Vancouver"],
    "Australia": ["Sydney", "Melbourne", "Brisbane"],
}


def _cities_for(country: str) -> list[str]:
    return _CITIES_BY_COUNTRY.get(country) or ["—"]


def render() -> None:
    page_title("The shortlist, not the brochure.", eyebrow="02 / MATCH")
    st.markdown(
        "<p class='speako-sub'>Ranked by outcome data and price fit. "
        "We don't take referral fees, so the rank means something.</p>",
        unsafe_allow_html=True,
    )

    _, categories, _ = load_pipelines()
    country_options = categories["Country"] if categories else _DEFAULT_COUNTRIES
    disease_options = categories["Disease"] if categories else None

    st.markdown(rule("FILTERS"), unsafe_allow_html=True)
    # No st.form — cascading dropdowns need immediate-mode rerun so changing
    # the country updates the city list before the user clicks RANK MATCHES.
    col1, col2, col3 = st.columns(3)
    with col1:
        if disease_options:
            disease = st.selectbox("PROCEDURE", disease_options)
        else:
            disease = st.text_input("PROCEDURE", "Heart Bypass")
    with col2:
        country = st.selectbox("COUNTRY", country_options, key="rec_country")
        city = st.selectbox("CITY", _cities_for(country), key=f"rec_city_{country}")
    with col3:
        budget = st.number_input("MAX BUDGET (USD)", 1000, 150000, 15000)

    submit = st.button("RANK MATCHES →", key="rec_submit", use_container_width=True)
    if not submit:
        return

    st.markdown(rule("HOSPITALS"), unsafe_allow_html=True)
    hospitals = get_hospitals(disease, country, city, budget)
    if hospitals:
        for idx, h in enumerate(hospitals, start=1):
            st.markdown(
                f"<div class='hairline-card' style='padding:18px;'>"
                f"<div class='cap sub'>{idx:02d} / RANKED</div>"
                f"<h4 style='margin:4px 0 10px 0; text-transform:uppercase; "
                f"letter-spacing:0.04em; font-size:15px;'>{h['Name']}</h4>"
                + leader_row("SPECIALIZATION", h["Specialization"])
                + leader_row("CITY", h["City"])
                + leader_row("PRICE BAND", h["Cost_Range"])
                + leader_row("RATING", f"{h['Rating']} / 5.0")
                + "</div>",
                unsafe_allow_html=True,
            )
            if st.button(f"REQUEST QUOTE / {h['Name'].upper()}", key=h["Name"]):
                st.success(f"Quote requested from {h['Name']}.")
    else:
        st.warning("No hospitals match this budget. Try raising it.")

    st.markdown(rule("SPECIALISTS"), unsafe_allow_html=True)
    for d in get_doctors(disease, country):
        st.markdown(
            f"<div class='hairline-card' style='padding:18px;'>"
            f"<h4 style='margin:0 0 8px 0; text-transform:uppercase; "
            f"letter-spacing:0.04em; font-size:14px;'>{d['Name']}</h4>"
            + leader_row("EXPERIENCE", d["Experience"])
            + leader_row("LANGUAGES", d["Language"])
            + "</div>",
            unsafe_allow_html=True,
        )
