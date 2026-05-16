"""Groq-backed symptom triage. Returns a dict with Disease/Department/Severity."""

import json
import os

from groq import Groq


_FALLBACK = {"Disease": "Diagnosis required", "Department": "General Consultation", "Severity": "Consult Doctor"}
_MODEL = "llama-3.3-70b-versatile"


def get_symptom_analysis(symptoms: str, api_key: str | None = None) -> dict:
    api_key = api_key or os.getenv("GROQ_API_KEY")
    if not api_key:
        return {"Disease": "Unable to predict without API Key", "Department": "General", "Severity": "Unknown"}

    try:
        client = Groq(api_key=api_key)
        prompt = (
            f"Analyze these symptoms: {symptoms}. Respond with a JSON object ONLY containing keys: "
            "'Disease' (most likely), 'Department' (medical department), and 'Severity' (Low, Medium, or High)."
        )
        response = client.chat.completions.create(
            model=_MODEL,
            messages=[
                {"role": "system", "content": "You output strictly valid JSON. No prose, no markdown."},
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0,
        )
        return json.loads(response.choices[0].message.content or "{}")
    except Exception:
        return _FALLBACK
