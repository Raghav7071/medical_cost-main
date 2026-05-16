"""One-off verification of the cost estimator. Delete after the task closes.

Runs six checks against the trained pipelines, using the exact input shown in
the user's screenshot, and reports the result as a structured block.
"""

import sys

import joblib
import pandas as pd

from config import PIPELINE_TARGETS, categories_path, pipeline_path


# Input from the screenshot's form.
SCREENSHOT_INPUTS = {
    "Disease": "Oncology",
    "Country": "Thailand",
    "Hospital_Type": "Public",
    "Stay_Days": 10,
    "Travel_Class": "First Class",
    "Room_Type": "VIP Suite",
    "Doctor_Experience": "10-20 Years",
    "Insurance": "No Insurance",
    "City": "Bangkok",
}

# Observed ranges from dataset.csv (filled in dynamically below).
def load_pipelines_direct() -> tuple[dict, dict]:
    """Same as ml.inference.load_pipelines but no Streamlit cache."""
    models = {t: joblib.load(pipeline_path(t)) for t in PIPELINE_TARGETS}
    categories = joblib.load(categories_path())
    return models, categories


def predict_costs(models: dict, inputs: dict) -> dict[str, float]:
    df = pd.DataFrame([inputs])
    return {t: float(m.predict(df)[0]) for t, m in models.items()}


def fmt(x: float) -> str:
    return f"${x:>14,.2f}"


def main() -> int:
    print("=" * 78)
    print(" MediGuide cost estimator — verification report")
    print("=" * 78)

    # ---- load -----------------------------------------------------------------
    try:
        models, categories = load_pipelines_direct()
    except Exception as e:
        print(f"\n[FATAL] Failed to load pipelines: {type(e).__name__}: {e}")
        return 1

    print(f"\nLoaded {len(models)} pipelines: {list(models.keys())}")
    print(f"Loaded {len(categories)} categorical column maps: {list(categories.keys())}")

    # Sanity: are the screenshot's categorical values present in the trained
    # category lists?
    print("\n— categorical-value membership check —")
    for col, value in SCREENSHOT_INPUTS.items():
        if col == "Stay_Days":
            continue
        valid = categories.get(col, [])
        ok = value in valid
        mark = "OK " if ok else "BAD"
        print(f"  [{mark}] {col:20s} = {value!r:30s} (trained values: {len(valid)})")
        if not ok:
            print(f"          Known values: {valid}")

    # ---- prediction -----------------------------------------------------------
    pred = predict_costs(models, SCREENSHOT_INPUTS)
    print("\n— prediction on screenshot inputs —")
    for k in PIPELINE_TARGETS:
        print(f"  {k:18s} {fmt(pred[k])}")

    # Check 1: output shape
    print("\n— Check 1: output shape —")
    keys_ok = set(pred.keys()) == set(PIPELINE_TARGETS)
    all_floats = all(isinstance(v, float) for v in pred.values())
    all_positive = all(v > 0 for v in pred.values())
    print(f"  exactly 5 expected keys present: {keys_ok}")
    print(f"  all values are floats:           {all_floats}")
    print(f"  all values are positive:         {all_positive}")

    # ---- ranges from dataset --------------------------------------------------
    df = pd.read_csv("dataset.csv")
    print("\n— Check 2: range vs. training data —")
    range_pass = True
    for t in PIPELINE_TARGETS:
        lo, hi = df[t].min(), df[t].max()
        v = pred[t]
        ok = lo <= v <= hi
        if not ok:
            range_pass = False
        mark = "OK " if ok else "BAD"
        print(f"  [{mark}] {t:18s} pred={fmt(v)}  range=[{fmt(lo)}, {fmt(hi)}]")
    print(f"  all-targets in training range:   {range_pass}")

    # ---- nearest-neighbour comparison ----------------------------------------
    # Per-target empirical comparison. Each target gets filtered on the
    # categoricals that genuinely drive it — otherwise we'd compare a First
    # Class + VIP Suite prediction against a median of economy + standard
    # rooms and falsely flag a healthy model.
    print("\n— Check 3: nearest-neighbour empirical comparison —")
    target_drivers = {
        "Treatment_Cost": ["Disease", "Country", "Hospital_Type", "Insurance"],
        "Travel_Cost":    ["Country", "Travel_Class"],
        "Stay_Cost":      ["Country", "Room_Type", "Hospital_Type"],  # also bands Stay_Days
        "Medicine_Cost":  ["Disease", "Country", "Insurance"],
        "Total_Cost":     ["Disease", "Country", "Hospital_Type", "Insurance"],
    }
    # For Stay_Cost we also narrow to nearby Stay_Days (numeric, so categorical
    # equality can't be used). Stay_Days drives Stay_Cost more than any
    # categorical does.
    stay_window = 2  # match Stay_Days ±2 days for Stay_Cost
    nn_pass = True
    any_skip = False
    for t in PIPELINE_TARGETS:
        drivers = target_drivers[t]
        m = pd.Series(True, index=df.index)
        for col in drivers:
            m &= df[col] == SCREENSHOT_INPUTS[col]
        if t == "Stay_Cost":
            target_days = SCREENSHOT_INPUTS["Stay_Days"]
            m &= df["Stay_Days"].between(target_days - stay_window, target_days + stay_window)
        sub = df[m]
        v = pred[t]
        if len(sub) == 0:
            print(f"  [SKIP] {t:18s} no rows matching {drivers}")
            any_skip = True
            continue
        med = sub[t].median()
        mean = sub[t].mean()
        ratio = v / med if med else float("inf")
        ok = 0.5 <= ratio <= 1.5
        if not ok:
            nn_pass = False
        mark = "OK " if ok else "WRN"
        print(
            f"  [{mark}] {t:18s} pred={fmt(v)}  med={fmt(med)}  "
            f"mean={fmt(mean)}  pred/med={ratio:.2f}x  n={len(sub):4d}  drivers={drivers}"
        )
    if any_skip:
        print("  (one or more targets had no matching rows; not counted against pass)")
    print(f"  matched-targets within ±50% of empirical median: {nn_pass}")

    # ---- Total_Cost coherence -------------------------------------------------
    print("\n— Check 4: Total_Cost coherence —")
    components = ["Treatment_Cost", "Travel_Cost", "Stay_Cost", "Medicine_Cost"]
    summed = sum(pred[c] for c in components)
    standalone = pred["Total_Cost"]
    delta = abs(summed - standalone) / max(standalone, 1)
    print(f"  sum of components:               {fmt(summed)}")
    print(f"  standalone Total_Cost model:     {fmt(standalone)}")
    print(f"  relative delta:                  {delta:.2%}")
    coherence_pass = delta <= 0.30
    print(f"  within 30% of each other:        {coherence_pass}")

    # ---- determinism ----------------------------------------------------------
    print("\n— Check 5: determinism —")
    pred2 = predict_costs(models, SCREENSHOT_INPUTS)
    deterministic = all(pred[k] == pred2[k] for k in PIPELINE_TARGETS)
    print(f"  predict_costs is deterministic:  {deterministic}")

    # ---- input sensitivity ----------------------------------------------------
    print("\n— Check 6: input sensitivity (Hospital_Type Public→Private) —")
    alt_inputs = dict(SCREENSHOT_INPUTS, Hospital_Type="Private")
    pred_alt = predict_costs(models, alt_inputs)
    treatment_delta = abs(pred_alt["Treatment_Cost"] - pred["Treatment_Cost"])
    sensitivity_ok = treatment_delta > 1.0  # > $1 difference is enough to prove signal
    print(f"  Treatment_Cost Public:           {fmt(pred['Treatment_Cost'])}")
    print(f"  Treatment_Cost Private:          {fmt(pred_alt['Treatment_Cost'])}")
    print(f"  absolute delta:                  {fmt(treatment_delta)}")
    print(f"  pipeline responds to category:   {sensitivity_ok}")

    # ---- verdict --------------------------------------------------------------
    print("\n" + "=" * 78)
    checks = {
        "1 shape":          keys_ok and all_floats and all_positive,
        "2 range":          range_pass,
        "3 neighbour":      nn_pass if nn_pass is not None else True,
        "4 coherence":      coherence_pass,
        "5 determinism":    deterministic,
        "6 sensitivity":    sensitivity_ok,
    }
    for name, ok in checks.items():
        print(f"  [{'PASS' if ok else 'FAIL'}] check {name}")
    all_pass = all(checks.values())
    print("=" * 78)
    print("  VERDICT:", "ESTIMATOR WORKING" if all_pass else "ISSUES FOUND — see above")
    print("=" * 78)
    return 0 if all_pass else 2


if __name__ == "__main__":
    sys.exit(main())
