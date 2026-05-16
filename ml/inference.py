"""The only module in the codebase that calls ``joblib.load`` at runtime.
UI code talks to :func:`load_pipelines` and :func:`predict_costs` instead of
touching disk directly."""

import joblib
import pandas as pd
import streamlit as st

from config import PIPELINE_TARGETS, categories_path, pipeline_path


@st.cache_resource
def load_pipelines() -> tuple[dict | None, dict | None, str | None]:
    """Returns (models, categories, error_message). Cached so disk hits happen
    once per session."""
    try:
        models = {target: joblib.load(pipeline_path(target)) for target in PIPELINE_TARGETS}
        categories = joblib.load(categories_path())
        return models, categories, None
    except Exception as e:
        return None, None, f"{type(e).__name__}: {e}"


def predict_costs(models: dict, inputs: dict) -> dict[str, float]:
    """Run every cost pipeline on a single input row."""
    input_df = pd.DataFrame([inputs])
    return {target: float(model.predict(input_df)[0]) for target, model in models.items()}
