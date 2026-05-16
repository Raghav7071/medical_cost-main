import os

import streamlit as st

from services.ocr import (
    classify_departments,
    extract_image_structured,
    extract_pdf_via_vision,
    extract_text_from_pdf,
)
from ui.components import page_title, rule


_IMAGE_EXTS = {"png", "jpg", "jpeg"}
# Below this character count we assume pdfplumber's embedded-text extraction
# came back empty (scanned PDF) and switch to the vision pipeline.
_PDF_EMBEDDED_TEXT_MIN = 40


def _extract(temp_path: str, ext: str, api_key: str | None):
    """Return a uniform dict for both image and PDF flows."""
    if ext.lower() in _IMAGE_EXTS:
        return extract_image_structured(temp_path, api_key=api_key)

    # PDF: try pdfplumber first (fast, free, perfect for digital reports).
    # If we get back little or no embedded text, the PDF is likely scanned —
    # render each page to an image and run vision OCR.
    pdf_text = extract_text_from_pdf(temp_path)
    is_error = pdf_text.startswith("PDF Error:")
    if not is_error and len(pdf_text.strip()) >= _PDF_EMBEDDED_TEXT_MIN:
        return {
            "text": pdf_text,
            "is_medical_document": True,
            "confidence": None,
            "reason": "Extracted via embedded text.",
            "error": None,
        }

    # Fall back: render pages → vision OCR.
    return extract_pdf_via_vision(temp_path, api_key=api_key)


def _confidence_html(confidence) -> str:
    if confidence is None:
        body = "<span style='font-size:22px;'>&mdash;</span>"
    else:
        body = f"{int(confidence)}<span style='font-size:18px;'>%</span>"
    return (
        "<div style='height:10px;'></div>"
        "<div class='cap sub'>CONFIDENCE</div>"
        f"<div class='numeric' style='font-size:32px; margin-top:4px;'>{body}</div>"
        "</div>"
    )


def _error_confidence_html() -> str:
    return (
        "<div style='height:10px;'></div>"
        "<div class='cap sub'>CONFIDENCE</div>"
        "<div class='numeric' style='font-size:22px; margin-top:4px; color:#b00020;'>ERROR</div>"
        "</div>"
    )


def render() -> None:
    page_title("Upload a report. Get structured data.", eyebrow="03 / INTAKE")
    st.markdown(
        "<p class='speako-sub'>PDFs, scans, phone photos. The extractor handles all of them. "
        "Handwriting it doesn't — nothing does.</p>",
        unsafe_allow_html=True,
    )

    st.markdown(rule("UPLOAD"), unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        file = st.file_uploader("PDF / PNG / JPG", type=["png", "jpg", "jpeg", "pdf"])
    with col2:
        img_camera = st.camera_input("OR CAPTURE LIVE")

    target_file = file or img_camera
    if not target_file:
        return

    api_key = st.session_state.get("groq_key") or os.getenv("GROQ_API_KEY")

    with st.spinner("running OCR..."):
        # Derive extension from the actual target. If a file was uploaded,
        # use its extension — st.camera_input may still hold a stale frame
        # from a previous interaction, so we can't infer "jpg" just because
        # img_camera is truthy.
        if file is not None:
            ext = file.name.split(".")[-1]
        else:
            ext = "jpg"
        temp_path = f"temp_upload.{ext}"
        try:
            with open(temp_path, "wb") as f:
                f.write(target_file.getbuffer())
            result = _extract(temp_path, ext, api_key)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    st.markdown(rule("RAW OUTPUT"), unsafe_allow_html=True)

    if result["error"]:
        st.error(result["error"])
    elif not result["is_medical_document"] and ext.lower() in _IMAGE_EXTS:
        warning = result["reason"] or "This image doesn't look like a medical document."
        st.warning(warning)

    c1, c2 = st.columns([2, 1])
    with c1:
        st.text_area(
            "EXTRACTED TEXT",
            result["text"] or "(no text extracted)",
            height=260,
            label_visibility="collapsed",
        )
    with c2:
        st.markdown(
            "<div class='hairline-card' style='padding:18px;'>"
            "<div class='cap sub'>SUGGESTED DEPARTMENTS</div>"
            "<div style='height:8px;'></div>",
            unsafe_allow_html=True,
        )
        departments = classify_departments(result["text"]) if result["text"] else ["—"]
        for d in departments:
            st.markdown(
                f"<div style='border:1px solid #0A0A0A; padding:8px 12px; "
                f"margin:0 0 6px 0; font-size:12px; text-transform:uppercase; "
                f"letter-spacing:0.06em; font-weight:700;'>{d}</div>",
                unsafe_allow_html=True,
            )

        if result["error"]:
            st.markdown(_error_confidence_html(), unsafe_allow_html=True)
        else:
            st.markdown(_confidence_html(result["confidence"]), unsafe_allow_html=True)
