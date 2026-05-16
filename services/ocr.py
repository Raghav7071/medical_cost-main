"""OCR + keyword classification for uploaded medical reports.

Image OCR is delegated to a Groq vision model. PDFs are first attempted via
pdfplumber for embedded text; if the PDF is a scan with no embedded text, we
render each page to an image with pypdfium2 and run them through the same
vision model.
"""

from __future__ import annotations

import base64
import io
import json
import mimetypes
import os
from typing import Optional, TypedDict

import pdfplumber
import pypdfium2 as pdfium
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# Max pages to render → vision. PDFs larger than this fall back to the
# pdfplumber output even if it's empty; we don't want a 100-page PDF burning
# 100 API calls.
_PDF_VISION_PAGE_LIMIT = 8
# Render scale for pypdfium2. 2.0 is roughly 144 DPI — readable for OCR
# without bloating the base64 payload.
_PDF_RENDER_SCALE = 2.0

_DEPARTMENT_KEYWORDS = {
    "Cardiology": ["heart", "bypass", "ecg", "blood pressure", "arrhythmia"],
    "Orthopedics": ["bone", "fracture", "joint", "knee", "spine", "fusion"],
    "Oncology": ["tumor", "cancer", "chemo", "malignant", "carcinoma"],
    "Neurology": ["brain", "nerve", "seizure", "migraine", "spinal"],
    "Dental": ["tooth", "cavity", "implant", "gum"],
}

_VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

_VISION_PROMPT = (
    "You are an OCR + triage assistant for a medical-intake tool. Look at the image and respond "
    "with a SINGLE JSON object and nothing else. Use exactly these keys:\n"
    '  "text": the verbatim text visible in the image, or "" if there is none.\n'
    '  "is_medical_document": true only if this looks like a medical report, prescription, lab '
    'result, discharge summary, scan, or similar clinical document. Selfies, screenshots of '
    'unrelated apps, random photos, etc. are false.\n'
    '  "confidence": integer 0-100 reflecting how confident you are in the extracted text. '
    'If the image is not a medical document, this should be low (0-20).\n'
    '  "reason": one short sentence explaining your confidence (e.g. "clear printed lab report", '
    '"image is a selfie, no document present", "handwriting illegible").\n'
    "Return only the JSON object, no markdown, no commentary."
)


class OcrResult(TypedDict):
    text: str
    is_medical_document: bool
    confidence: Optional[int]
    reason: str
    error: Optional[str]


def _empty_result(error: Optional[str] = None) -> OcrResult:
    return {
        "text": "",
        "is_medical_document": False,
        "confidence": 0 if error else None,
        "reason": "",
        "error": error,
    }


def _resolve_api_key(api_key: Optional[str]) -> Optional[str]:
    return api_key or os.getenv("GROQ_API_KEY")


def _encode_image(image_path: str) -> tuple[str, str]:
    mime, _ = mimetypes.guess_type(image_path)
    if not mime or not mime.startswith("image/"):
        mime = "image/jpeg"
    with open(image_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return mime, b64


def extract_image_structured(image_path: str, api_key: Optional[str] = None) -> OcrResult:
    """Run Groq vision OCR. Never raises — failures are reported in result['error']."""
    key = _resolve_api_key(api_key)
    if not key:
        return _empty_result(
            "Groq API key missing. Set GROQ_API_KEY in your .env file or paste it in the sidebar."
        )

    try:
        mime, b64 = _encode_image(image_path)
    except Exception as e:
        return _empty_result(f"Could not read image: {e}")

    try:
        client = Groq(api_key=key)
        resp = client.chat.completions.create(
            model=_VISION_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": _VISION_PROMPT},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:{mime};base64,{b64}"},
                        },
                    ],
                }
            ],
            temperature=0,
            max_tokens=1024,
        )
        raw = resp.choices[0].message.content or ""
    except Exception as e:
        return _empty_result(f"Groq vision call failed: {e}")

    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:]
        cleaned = cleaned.strip()

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        return _empty_result(
            "Groq returned a non-JSON response. Raw output: " + raw[:200]
        )

    text = str(data.get("text", "")).strip()
    is_medical = bool(data.get("is_medical_document", False))
    reason = str(data.get("reason", "")).strip()

    try:
        confidence = int(data.get("confidence", 0))
    except (TypeError, ValueError):
        confidence = 0
    confidence = max(0, min(100, confidence))

    return {
        "text": text,
        "is_medical_document": is_medical,
        "confidence": confidence,
        "reason": reason,
        "error": None,
    }


def extract_text_from_pdf(pdf_path: str) -> str:
    try:
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += (page.extract_text() or "") + "\n"
        return text
    except Exception as e:
        return f"PDF Error: {e}"


def extract_pdf_via_vision(pdf_path: str, api_key: Optional[str] = None) -> OcrResult:
    """Render PDF pages to images and run the vision OCR on each. Used as a
    fallback when pdfplumber returns no embedded text (scanned PDFs)."""
    key = _resolve_api_key(api_key)
    if not key:
        return _empty_result(
            "Groq API key missing. Set GROQ_API_KEY in your .env file or paste it in the sidebar."
        )

    try:
        doc = pdfium.PdfDocument(pdf_path)
    except Exception as e:
        return _empty_result(f"Could not open PDF: {e}")

    page_count = len(doc)
    if page_count == 0:
        return _empty_result("PDF has no pages.")

    pages_to_process = min(page_count, _PDF_VISION_PAGE_LIMIT)
    page_results: list[OcrResult] = []

    for i in range(pages_to_process):
        try:
            pil = doc[i].render(scale=_PDF_RENDER_SCALE).to_pil()
            buf = io.BytesIO()
            pil.convert("RGB").save(buf, format="JPEG", quality=85)
            b64 = base64.b64encode(buf.getvalue()).decode("ascii")
        except Exception as e:
            page_results.append(_empty_result(f"Page {i + 1}: render failed: {e}"))
            continue

        try:
            client = Groq(api_key=key)
            resp = client.chat.completions.create(
                model=_VISION_MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": _VISION_PROMPT},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{b64}"},
                            },
                        ],
                    }
                ],
                temperature=0,
                max_tokens=1024,
            )
            raw = resp.choices[0].message.content or ""
        except Exception as e:
            page_results.append(_empty_result(f"Page {i + 1}: vision call failed: {e}"))
            continue

        cleaned = raw.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.strip("`")
            if cleaned.lower().startswith("json"):
                cleaned = cleaned[4:]
            cleaned = cleaned.strip()
        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError:
            page_results.append(_empty_result(f"Page {i + 1}: non-JSON response."))
            continue

        try:
            conf = max(0, min(100, int(data.get("confidence", 0))))
        except (TypeError, ValueError):
            conf = 0
        page_results.append({
            "text": str(data.get("text", "")).strip(),
            "is_medical_document": bool(data.get("is_medical_document", False)),
            "confidence": conf,
            "reason": str(data.get("reason", "")).strip(),
            "error": None,
        })

    # Aggregate: concatenate text, take max confidence, OR on is_medical_document.
    texts = [r["text"] for r in page_results if r["text"]]
    confidences = [r["confidence"] for r in page_results if r["confidence"] is not None]
    errors = [r["error"] for r in page_results if r["error"]]

    if not texts and errors:
        return _empty_result("; ".join(errors[:3]))

    note = ""
    if page_count > pages_to_process:
        note = f" (showing first {pages_to_process} of {page_count} pages)"

    return {
        "text": "\n\n".join(texts),
        "is_medical_document": any(r["is_medical_document"] for r in page_results),
        "confidence": max(confidences) if confidences else 0,
        "reason": (page_results[0]["reason"] if page_results else "") + note,
        "error": None,
    }


def classify_departments(text: str) -> list[str]:
    text = text.lower()
    detected = [dept for dept, words in _DEPARTMENT_KEYWORDS.items() if any(w in text for w in words)]
    return list(set(detected)) if detected else ["General Medicine"]
