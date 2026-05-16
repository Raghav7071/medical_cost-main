"""Centralized paths and constants. Keep filesystem locations in one place."""

DB_NAME = "mediguide.db"
DATASET_CSV = "dataset.csv"
MODELS_DIR = "models"

# ML pipeline names (used for both training and inference).
PIPELINE_TARGETS = ["Treatment_Cost", "Travel_Cost", "Stay_Cost", "Medicine_Cost", "Total_Cost"]


def pipeline_path(target: str) -> str:
    return f"{MODELS_DIR}/{target.lower()}_pipeline.pkl"


def categories_path() -> str:
    return f"{MODELS_DIR}/categories.pkl"
