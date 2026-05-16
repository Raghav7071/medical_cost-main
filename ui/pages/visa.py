"""Medical Visa & Travel Assistance — helps patients traveling abroad for
treatment with visa requirements, hospital finder, stay planning, and
emergency contacts."""

import streamlit as st
from ui.components import page_title


# ── static data ──────────────────────────────────────────────────────────────

COUNTRIES = {
    "India": {
        "flag": "🇮🇳",
        "visa_type": "e-Medical Visa",
        "duration": "60 days (triple entry)",
        "documents": [
            "Valid passport (6+ months)",
            "Medical invitation from hospital",
            "Proof of financial means",
            "Return ticket confirmation",
            "Medical records / referral letter",
        ],
        "insurance": "Travel medical insurance recommended (not mandatory)",
        "hospitals": [
            {"name": "Apollo Hospitals, Chennai", "specialty": "Cardiac Surgery", "rating": 4.8},
            {"name": "Fortis Memorial, Gurugram", "specialty": "Oncology", "rating": 4.7},
            {"name": "AIIMS, New Delhi", "specialty": "General", "rating": 4.9},
        ],
        "emergency": "112",
        "ambulance": "108 / 102",
        "guidelines": "India offers one of the most affordable healthcare systems globally. "
                      "Major cities have JCI-accredited hospitals with English-speaking staff.",
    },
    "Thailand": {
        "flag": "🇹🇭",
        "visa_type": "Medical Treatment Visa (Non-Immigrant MT)",
        "duration": "90 days (extendable)",
        "documents": [
            "Valid passport (6+ months)",
            "Hospital acceptance letter",
            "Proof of treatment plan",
            "Financial evidence (≥ $2,000)",
            "Two passport-size photos",
        ],
        "insurance": "Mandatory health insurance with COVID-19 coverage",
        "hospitals": [
            {"name": "Bumrungrad International", "specialty": "Multi-specialty", "rating": 4.9},
            {"name": "Bangkok Hospital", "specialty": "Orthopedics", "rating": 4.7},
            {"name": "Samitivej Hospital", "specialty": "Pediatrics", "rating": 4.6},
        ],
        "emergency": "1669",
        "ambulance": "1669",
        "guidelines": "Thailand is a top medical tourism destination, especially for cosmetic "
                      "surgery, dental work, and orthopedic procedures.",
    },
    "Turkey": {
        "flag": "🇹🇷",
        "visa_type": "Medical e-Visa",
        "duration": "90 days within 180 days",
        "documents": [
            "Valid passport",
            "Hospital appointment confirmation",
            "Health insurance document",
            "Proof of accommodation",
            "Bank statement (last 3 months)",
        ],
        "insurance": "Comprehensive health insurance required",
        "hospitals": [
            {"name": "Acıbadem Healthcare Group", "specialty": "Transplant", "rating": 4.8},
            {"name": "Memorial Hospital", "specialty": "Cardiac", "rating": 4.7},
            {"name": "Liv Hospital", "specialty": "Oncology", "rating": 4.6},
        ],
        "emergency": "112",
        "ambulance": "112",
        "guidelines": "Turkey has emerged as a leading medical tourism hub, particularly for "
                      "hair transplants, dental care, and eye surgery.",
    },
    "Singapore": {
        "flag": "🇸🇬",
        "visa_type": "Medical Visit Pass",
        "duration": "30 days (extendable)",
        "documents": [
            "Valid passport (6+ months)",
            "Hospital referral letter",
            "Proof of funds",
            "Completed Form 14A",
            "Treatment plan from hospital",
        ],
        "insurance": "Highly recommended, not mandatory for visa",
        "hospitals": [
            {"name": "Mount Elizabeth Hospital", "specialty": "Oncology", "rating": 4.9},
            {"name": "Gleneagles Hospital", "specialty": "Cardiac", "rating": 4.8},
            {"name": "Raffles Hospital", "specialty": "Multi-specialty", "rating": 4.7},
        ],
        "emergency": "995",
        "ambulance": "995",
        "guidelines": "Singapore offers world-class healthcare with some of the best medical "
                      "outcomes in Asia. Costs are higher than India or Thailand.",
    },
    "Germany": {
        "flag": "🇩🇪",
        "visa_type": "Medical Treatment Visa (Schengen)",
        "duration": "Up to 90 days",
        "documents": [
            "Valid passport",
            "Hospital appointment letter",
            "Proof of medical insurance (€30,000 min)",
            "Financial proof / sponsorship",
            "Accommodation confirmation",
        ],
        "insurance": "Mandatory travel health insurance (€30,000 coverage)",
        "hospitals": [
            {"name": "Charité Berlin", "specialty": "Research & General", "rating": 4.9},
            {"name": "University Hospital Heidelberg", "specialty": "Oncology", "rating": 4.8},
            {"name": "Munich Heart Center", "specialty": "Cardiac", "rating": 4.8},
        ],
        "emergency": "112",
        "ambulance": "112",
        "guidelines": "Germany is renowned for advanced oncology, orthopedics, and cardiac "
                      "surgery. Expect thorough, methodical care with longer consultations.",
    },
}

TRAVEL_CHECKLIST = [
    "Passport with 6+ months validity",
    "Medical visa (approved)",
    "Hospital appointment confirmation",
    "Medical records and referral letters",
    "Health insurance documents",
    "Prescription medicines (with doctor's note)",
    "Emergency contact card",
    "Travel adapter & phone charger",
    "Local currency / travel card",
    "Accommodation booking confirmation",
    "Return flight ticket",
    "Translator app downloaded",
]


# ── render ───────────────────────────────────────────────────────────────────

def render() -> None:
    page_title("Medical Visa & Travel Assistance", eyebrow="GLOBAL CARE")

    st.markdown(
        "<p style='color: #5B7185; font-size: 16px; margin-bottom: 32px;'>"
        "Planning to travel abroad for medical treatment? We'll guide you "
        "through visa requirements, hospital selection, and travel logistics."
        "</p>",
        unsafe_allow_html=True,
    )

    # ── country selector ─────────────────────────────────────────────────
    country_names = list(COUNTRIES.keys())

    st.markdown(
        "<div style='margin-bottom: 8px; font-weight: 600; color: #1E3A5F;'>"
        "Select Destination Country</div>",
        unsafe_allow_html=True,
    )

    # Country cards row
    cols = st.columns(len(country_names))
    for idx, (col, name) in enumerate(zip(cols, country_names)):
        with col:
            info = COUNTRIES[name]
            selected = st.session_state.get("visa_country") == name
            border = "1.5px solid #3B82F6" if selected else "1px solid #E4ECF3"
            bg = "#EAF4FF" if selected else "#FFFFFF"
            if st.button(
                f"{info['flag']} {name}",
                key=f"visa_country_{name}",
                use_container_width=True,
            ):
                st.session_state["visa_country"] = name
                st.rerun()

    selected_country = st.session_state.get("visa_country", country_names[0])
    data = COUNTRIES[selected_country]

    st.markdown("<div style='height: 32px;'></div>", unsafe_allow_html=True)

    # ── visa overview cards ──────────────────────────────────────────────
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f"<div class='hairline-card' style='border-top: 3px solid #3B82F6;'>"
            f"<div style='font-size: 13px; color: #5B7185; font-weight: 600; "
            f"text-transform: uppercase;'>Visa Type</div>"
            f"<div style='font-size: 20px; font-weight: 700; color: #1E3A5F; "
            f"margin-top: 8px;'>{data['visa_type']}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"<div class='hairline-card' style='border-top: 4px solid #10B981;'>"
            f"<div style='font-size: 13px; color: #5B7185; font-weight: 600; "
            f"text-transform: uppercase;'>Stay Duration</div>"
            f"<div style='font-size: 20px; font-weight: 700; color: #1E3A5F; "
            f"margin-top: 8px;'>{data['duration']}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f"<div class='hairline-card' style='border-top: 4px solid #F59E0B;'>"
            f"<div style='font-size: 13px; color: #5B7185; font-weight: 600; "
            f"text-transform: uppercase;'>Emergency Number</div>"
            f"<div style='font-size: 20px; font-weight: 700; color: #1E3A5F; "
            f"margin-top: 8px;'>📞 {data['emergency']}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

    # ── required documents ───────────────────────────────────────────────
    col_left, col_right = st.columns(2)

    with col_left:
        docs_html = "".join(
            f"<div style='display: flex; align-items: center; gap: 10px; "
            f"padding: 12px 0; border-bottom: 1px solid #F1F5F9;'>"
            f"<span style='color: #10B981; font-size: 16px;'>✓</span>"
            f"<span style='color: #334155; font-size: 14px;'>{doc}</span>"
            f"</div>"
            for doc in data["documents"]
        )
        st.markdown(
            f"<div class='hairline-card'>"
            f"<h4 style='margin-top: 0; color: #1E3A5F;'>📋 Required Documents</h4>"
            f"{docs_html}"
            f"</div>",
            unsafe_allow_html=True,
        )

    with col_right:
        st.markdown(
            f"<div class='hairline-card'>"
            f"<h4 style='margin-top: 0; color: #1E3A5F;'>🛡️ Insurance Requirement</h4>"
            f"<p style='color: #475569; line-height: 1.6;'>{data['insurance']}</p>"
            f"<div style='height: 16px;'></div>"
            f"<h4 style='margin-top: 0; color: #1E3A5F;'>ℹ️ Healthcare Guidelines</h4>"
            f"<p style='color: #475569; line-height: 1.6;'>{data['guidelines']}</p>"
            f"</div>",
            unsafe_allow_html=True,
        )

    # ── top hospitals ────────────────────────────────────────────────────
    st.markdown(
        f"<h3 style='margin: 32px 0 16px 0;'>🏥 Recommended Hospitals in "
        f"{data['flag']} {selected_country}</h3>",
        unsafe_allow_html=True,
    )

    hosp_cols = st.columns(len(data["hospitals"]))
    for col, hosp in zip(hosp_cols, data["hospitals"]):
        with col:
            stars = "⭐" * int(hosp["rating"])
            st.markdown(
                f"<div class='hairline-card' style='text-align: center;'>"
                f"<div style='font-size: 18px; font-weight: 700; color: #1E3A5F; "
                f"margin-bottom: 8px;'>{hosp['name']}</div>"
                f"<div style='display: inline-block; background: #EAF4FF; "
                f"color: #3B82F6; padding: 4px 12px; border-radius: 20px; "
                f"font-size: 13px; font-weight: 600; margin-bottom: 12px;'>"
                f"{hosp['specialty']}</div>"
                f"<div style='color: #F59E0B; font-size: 14px;'>"
                f"{stars} {hosp['rating']}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

    # ── emergency & ambulance ────────────────────────────────────────────
    e1, e2 = st.columns(2)
    with e1:
        st.markdown(
            f"<div class='hairline-card' style='background: #FEF2F2; "
            f"border-left: 3px solid #DC2626;'>"
            f"<h4 style='margin-top: 0; color: #DC2626;'>🚨 Emergency SOS</h4>"
            f"<p style='font-size: 32px; font-weight: 700; color: #EF4444; "
            f"margin: 8px 0;'>{data['emergency']}</p>"
            f"<p style='color: #5B7185; font-size: 14px;'>Emergency number for "
            f"{selected_country}</p>"
            f"</div>",
            unsafe_allow_html=True,
        )
    with e2:
        st.markdown(
            f"<div class='hairline-card' style='background: #D7F0EA; "
            f"border-left: 3px solid #0F9D7A;'>"
            f"<h4 style='margin-top: 0; color: #059669;'>🚑 Ambulance Service</h4>"
            f"<p style='font-size: 32px; font-weight: 700; color: #059669; "
            f"margin: 8px 0;'>{data['ambulance']}</p>"
            f"<p style='color: #5B7185; font-size: 14px;'>Ambulance helpline for "
            f"{selected_country}</p>"
            f"</div>",
            unsafe_allow_html=True,
        )

    # ── travel checklist ─────────────────────────────────────────────────
    st.markdown(
        "<h3 style='margin: 40px 0 16px 0;'>✅ Travel Checklist</h3>",
        unsafe_allow_html=True,
    )

    checklist_key = f"checklist_{selected_country}"
    if checklist_key not in st.session_state:
        st.session_state[checklist_key] = [False] * len(TRAVEL_CHECKLIST)

    total = len(TRAVEL_CHECKLIST)

    # Reserve a slot for the progress bar; we'll fill it AFTER the checkboxes
    # render so the count reflects the user's latest click (otherwise the
    # displayed total lags one click behind state).
    progress_slot = st.empty()

    checks = st.session_state[checklist_key]
    cl1, cl2 = st.columns(2)
    half = total // 2
    for ci, (col, items) in enumerate(
        [(cl1, TRAVEL_CHECKLIST[:half]), (cl2, TRAVEL_CHECKLIST[half:])]
    ):
        with col:
            for j, item in enumerate(items):
                real_idx = j if ci == 0 else j + half
                checks[real_idx] = st.checkbox(
                    item,
                    value=checks[real_idx],
                    key=f"chk_{selected_country}_{real_idx}",
                )
    st.session_state[checklist_key] = checks

    done = sum(checks)
    pct = int(done / total * 100)
    progress_slot.markdown(
        f"<div style='margin-bottom: 20px;'>"
        f"<div style='display: flex; justify-content: space-between; "
        f"margin-bottom: 8px;'>"
        f"<span style='font-weight: 600; color: #1E3A5F;'>"
        f"{done} of {total} completed</span>"
        f"<span style='color: #3B82F6; font-weight: 600;'>{pct}%</span></div>"
        f"<div style='width: 100%; background: #E4ECF3; border-radius: 8px; "
        f"height: 10px; overflow: hidden;'>"
        f"<div style='width: {pct}%; height: 100%; border-radius: 8px; "
        f"background: #3B82F6; "
        f"transition: width 0.4s ease;'></div>"
        f"</div></div>",
        unsafe_allow_html=True,
    )

    # ── visa status tracker (mock) ───────────────────────────────────────
    st.markdown(
        "<h3 style='margin: 40px 0 16px 0;'>📊 Visa Application Status</h3>",
        unsafe_allow_html=True,
    )

    steps = [
        ("Documents Collected", True),
        ("Application Submitted", True),
        ("Under Review", True),
        ("Interview Scheduled", False),
        ("Visa Approved", False),
    ]

    status_html = "<div style='display: flex; gap: 0; align-items: center; flex-wrap: wrap;'>"
    for i, (label, done_flag) in enumerate(steps):
        bg = "#3B82F6" if done_flag else "#E4ECF3"
        fg = "#FFFFFF" if done_flag else "#94A3B8"
        icon = "✓" if done_flag else str(i + 1)
        status_html += (
            f"<div style='display: flex; align-items: center;'>"
            f"<div style='width: 36px; height: 36px; border-radius: 50%; "
            f"background: {bg}; color: {fg}; display: flex; align-items: center; "
            f"justify-content: center; font-weight: 700; font-size: 14px;'>{icon}</div>"
            f"<div style='margin-left: 8px; margin-right: 20px;'>"
            f"<div style='font-size: 13px; font-weight: 600; color: "
            f"{'#1E3A5F' if done_flag else '#94A3B8'};'>{label}</div></div>"
            f"</div>"
        )
    status_html += "</div>"
    st.markdown(status_html, unsafe_allow_html=True)
