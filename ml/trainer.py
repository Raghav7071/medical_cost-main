"""Train one RandomForest pipeline per cost target and persist them, plus
a categories.pkl mapping used to populate UI dropdowns."""

import os

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from config import DATASET_CSV, MODELS_DIR, PIPELINE_TARGETS, categories_path, pipeline_path

CATEGORICAL_COLS = [
    "Disease", "Country", "Hospital_Type", "Travel_Class",
    "Room_Type", "Doctor_Experience", "Insurance", "City",
]
NUMERIC_FEATURES = ["Stay_Days"]


def _build_preprocessor() -> ColumnTransformer:
    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUMERIC_FEATURES),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL_COLS),
        ]
    )


def train_models(dataset_path: str = DATASET_CSV) -> None:
    os.makedirs(MODELS_DIR, exist_ok=True)
    df = pd.read_csv(dataset_path, keep_default_na=False)

    X = df[CATEGORICAL_COLS + NUMERIC_FEATURES]
    Y = df[PIPELINE_TARGETS]
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

    # Persist the category lists for the UI dropdowns.
    unique_categories = {col: df[col].unique().tolist() for col in CATEGORICAL_COLS}
    joblib.dump(unique_categories, categories_path())

    print("Training pipelines...")
    for target in PIPELINE_TARGETS:
        pipeline = Pipeline(
            steps=[
                ("preprocessor", _build_preprocessor()),
                ("model", RandomForestRegressor(n_estimators=100, random_state=42)),
            ]
        )
        pipeline.fit(X_train, y_train[target])
        r2 = r2_score(y_test[target], pipeline.predict(X_test))
        print(f"  {target} R² = {r2:.4f}")
        joblib.dump(pipeline, pipeline_path(target))
