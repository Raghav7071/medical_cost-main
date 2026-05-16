"""Synthetic medical-tourism dataset generator. Numeric behavior is identical
to the previous monolithic train_model.py:generate_dataset."""

import numpy as np
import pandas as pd

from config import DATASET_CSV

DISEASES = [
    "Heart Bypass", "Knee Replacement", "Spinal Fusion", "Cataract Surgery",
    "Dental Implants", "Cosmetic Surgery", "Oncology", "Neurology", "Orthopedics",
]
COUNTRIES = [
    "USA", "UK", "Canada", "Australia", "Germany", "France", "UAE",
    "India", "Thailand", "Turkey", "Singapore",
]
HOSPITAL_TYPES = ["Public", "Private", "Premium International", "Luxury Medical Resort"]
DOCTOR_EXPERIENCES = ["1-5 Years", "5-10 Years", "10-20 Years", "20+ Years"]
TRAVEL_CLASSES = ["Economy", "Business", "First Class"]
ROOM_TYPES = ["General Ward", "Semi-Private", "Private", "VIP Suite"]
INSURANCES = ["No Insurance", "Partial", "Full"]
CITIES = ["New York", "London", "Dubai", "Singapore", "Bangkok", "Istanbul", "Mumbai"]


def _row(rng) -> dict:
    disease = rng.choice(DISEASES)
    country = rng.choice(COUNTRIES)
    hospital_type = rng.choice(HOSPITAL_TYPES)
    doctor_exp = rng.choice(DOCTOR_EXPERIENCES)
    travel_class = rng.choice(TRAVEL_CLASSES)
    room_type = rng.choice(ROOM_TYPES)
    insurance = rng.choice(INSURANCES)
    city = rng.choice(CITIES)

    stay_days = rng.randint(1, 45)

    treatment_cost = rng.uniform(3000, 25000)
    if disease in ("Heart Bypass", "Oncology", "Neurology"):
        treatment_cost *= 2.5
    elif disease in ("Dental Implants", "Cataract Surgery"):
        treatment_cost *= 0.4
    if hospital_type == "Premium International":
        treatment_cost *= 1.5
    elif hospital_type == "Luxury Medical Resort":
        treatment_cost *= 2.5
    if doctor_exp == "20+ Years":
        treatment_cost *= 1.3

    travel_cost = rng.uniform(500, 2000)
    if travel_class == "Business":
        travel_cost *= 3
    elif travel_class == "First Class":
        travel_cost *= 6

    daily_room_rate = 100
    if room_type == "Semi-Private":
        daily_room_rate = 200
    elif room_type == "Private":
        daily_room_rate = 500
    elif room_type == "VIP Suite":
        daily_room_rate = 1500
    stay_cost = daily_room_rate * stay_days

    medicine_cost = treatment_cost * rng.uniform(0.05, 0.20)

    treatment_cost += rng.normal(0, treatment_cost * 0.05)
    travel_cost += rng.normal(0, travel_cost * 0.05)
    stay_cost += rng.normal(0, stay_cost * 0.05)
    medicine_cost += rng.normal(0, medicine_cost * 0.05)

    total_cost = treatment_cost + travel_cost + stay_cost + medicine_cost
    if insurance == "Partial":
        total_cost *= 0.6
    elif insurance == "Full":
        total_cost *= 0.1

    return {
        "Disease": disease,
        "Country": country,
        "Hospital_Type": hospital_type,
        "Stay_Days": stay_days,
        "Travel_Class": travel_class,
        "Room_Type": room_type,
        "Doctor_Experience": doctor_exp,
        "Insurance": insurance,
        "City": city,
        "Treatment_Cost": round(treatment_cost, 2),
        "Travel_Cost": round(travel_cost, 2),
        "Stay_Cost": round(stay_cost, 2),
        "Medicine_Cost": round(medicine_cost, 2),
        "Total_Cost": round(total_cost, 2),
    }


def generate_dataset(num_rows: int = 10000, seed: int = 42, out_path: str = DATASET_CSV) -> pd.DataFrame:
    print("Generating MediGuide AI dataset...")
    rng = np.random.RandomState(seed)
    df = pd.DataFrame([_row(rng) for _ in range(num_rows)])
    df.to_csv(out_path, index=False)
    print(f"Dataset generated with {num_rows} rows -> {out_path}")
    return df
