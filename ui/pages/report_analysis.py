import time
import streamlit as st
from ui.components import page_title

def render() -> None:
    page_title("Medical Report Analysis", eyebrow="AI DIAGNOSTICS")
    
    st.markdown(
        "<p style='color: #5B7185; font-size: 16px; margin-bottom: 24px;'>"
        "Upload your lab reports or prescriptions for instant AI analysis, risk assessment, and personalized health recommendations."
        "</p>",
        unsafe_allow_html=True
    )

    if "report_history" not in st.session_state:
        st.session_state.report_history = []

    # Upload Section
    st.markdown(
        "<div class='hairline-card' style='text-align: center; padding: 40px;'>"
        "<h3 style='margin: 0 0 16px 0; color: #1E3A5F;'>Upload Medical Document</h3>"
        "<p style='color: #5B7185; font-size: 14px; margin-bottom: 24px;'>Supports PDF, JPG, PNG (Max 10MB)</p>",
        unsafe_allow_html=True
    )
    
    uploaded_file = st.file_uploader("", type=["pdf", "png", "jpg", "jpeg"], label_visibility="collapsed")
    
    if uploaded_file and st.button("Analyze Report", type="primary", use_container_width=True):
        with st.spinner("Extracting text and analyzing medical data..."):
            time.sleep(2.5) # Simulate OCR and AI processing
            
            # Mock AI Result
            analysis = {
                "date": time.strftime("%Y-%m-%d %H:%M"),
                "filename": uploaded_file.name,
                "symptoms": ["Elevated fasting glucose", "High LDL cholesterol", "Fatigue reported"],
                "abnormal_values": [
                    {"marker": "HbA1c", "value": "6.8%", "status": "High"},
                    {"marker": "LDL Cholesterol", "value": "145 mg/dL", "status": "High"}
                ],
                "risk_level": "Medium",
                "disease_prediction": "Pre-diabetes & Mild Hyperlipidemia",
                "health_summary": "The blood report indicates elevated blood sugar levels consistent with pre-diabetes and higher-than-normal LDL cholesterol. No immediate emergency detected, but lifestyle modifications are strongly recommended.",
                "doctor": "Endocrinologist / General Physician",
                "medicines": "Consult doctor for possible statins or Metformin. (No prescription provided by AI)",
                "diet": "Low carb, high fiber diet. Reduce refined sugars and saturated fats. Increase omega-3 intake.",
                "emergency": False
            }
            st.session_state.report_history.insert(0, analysis)
            st.success("Analysis complete!")
    
    st.markdown("</div>", unsafe_allow_html=True)

    # Show latest analysis if exists
    if st.session_state.report_history:
        latest = st.session_state.report_history[0]
        
        # Dashboard layout for results
        st.markdown("<h3 style='margin: 32px 0 16px 0;'>Latest Analysis Results</h3>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        risk_color = "#F59E0B" if latest["risk_level"] == "Medium" else "#10B981"
        if latest["risk_level"] == "High": risk_color = "#EF4444"
            
        with col1:
            st.markdown(
                f"<div class='hairline-card' style='text-align: center; border-top: 4px solid {risk_color};'>"
                f"<div style='font-size: 13px; color: #5B7185; font-weight: 600; text-transform: uppercase;'>Risk Level</div>"
                f"<div style='font-size: 32px; font-weight: 700; color: {risk_color}; margin-top: 8px;'>{latest['risk_level']}</div>"
                f"</div>",
                unsafe_allow_html=True
            )
        with col2:
            st.markdown(
                f"<div class='hairline-card' style='text-align: center; border-top: 4px solid #3B82F6;'>"
                f"<div style='font-size: 13px; color: #5B7185; font-weight: 600; text-transform: uppercase;'>Predicted Condition</div>"
                f"<div style='font-size: 18px; font-weight: 700; color: #1E3A5F; margin-top: 8px;'>{latest['disease_prediction']}</div>"
                f"</div>",
                unsafe_allow_html=True
            )
        with col3:
            st.markdown(
                f"<div class='hairline-card' style='text-align: center; border-top: 4px solid #8B5CF6;'>"
                f"<div style='font-size: 13px; color: #5B7185; font-weight: 600; text-transform: uppercase;'>Recommended Specialist</div>"
                f"<div style='font-size: 18px; font-weight: 700; color: #1E3A5F; margin-top: 8px;'>{latest['doctor']}</div>"
                f"</div>",
                unsafe_allow_html=True
            )

        # Detailed cards
        st.markdown(
            f"<div class='hairline-card'>"
            f"<h4 style='margin-top: 0;'>AI Health Summary</h4>"
            f"<p style='color: #475569; line-height: 1.6;'>{latest['health_summary']}</p>"
            f"</div>",
            unsafe_allow_html=True
        )

        c1, c2 = st.columns(2)
        with c1:
            abnormal_html = "".join([f"<div style='display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #E4ECF3;'><span>{item['marker']}</span><span style='color: #EF4444; font-weight: 600;'>{item['value']}</span></div>" for item in latest["abnormal_values"]])
            st.markdown(
                f"<div class='hairline-card' style='height: 100%;'>"
                f"<h4 style='margin-top: 0;'>⚠️ Abnormal Values</h4>"
                f"{abnormal_html}"
                f"</div>",
                unsafe_allow_html=True
            )
        with c2:
            st.markdown(
                f"<div class='hairline-card' style='height: 100%;'>"
                f"<h4 style='margin-top: 0;'>🥗 Recommendations</h4>"
                f"<p><strong>Diet:</strong> {latest['diet']}</p>"
                f"<p><strong>Medicines:</strong> {latest['medicines']}</p>"
                f"</div>",
                unsafe_allow_html=True
            )
            
        if st.button("📄 Download Full Report (PDF)", use_container_width=True):
            st.toast("Downloading PDF...")
            
    # History
    if len(st.session_state.report_history) > 1:
        st.markdown("<h3 style='margin: 40px 0 16px 0;'>Report History</h3>", unsafe_allow_html=True)
        for idx, past in enumerate(st.session_state.report_history[1:]):
            st.markdown(
                f"<div style='padding: 16px; background: #FFFFFF; border: 1px solid #E4ECF3; border-radius: 12px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center;'>"
                f"<div>"
                f"<div style='font-weight: 600; color: #1E3A5F;'>{past['filename']}</div>"
                f"<div style='font-size: 13px; color: #5B7185;'>{past['date']} • {past['disease_prediction']}</div>"
                f"</div>"
                f"<div style='color: #3B82F6; font-weight: 500; cursor: pointer;'>View</div>"
                f"</div>",
                unsafe_allow_html=True
            )
