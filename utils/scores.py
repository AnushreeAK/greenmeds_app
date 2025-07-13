import pandas as pd
from difflib import get_close_matches

df = pd.read_csv("data/meds_info.csv")

def get_medicine_data(medicine_name):
    if not isinstance(medicine_name, str) or not medicine_name.strip():
        return None

    medicine_name_cleaned = medicine_name.strip().lower()
    all_meds = df["medicine"].dropna().astype(str)
    all_meds_lower = all_meds.str.lower()

    # Exact Match
    exact_match = df[all_meds_lower == medicine_name_cleaned]
    if not exact_match.empty:
        return exact_match.iloc[0].to_dict()

    # Fuzzy Match
    matches = get_close_matches(medicine_name_cleaned, all_meds_lower.tolist(), n=5, cutoff=0.5)
    if matches:
        return {"fallback": list(dict.fromkeys(matches))}

    return None

def calculate_eco_score(data):
    score = 100
    if data['toxicity_level'].lower() == "high":
        score -= 50
    elif data['toxicity_level'].lower() == "medium":
        score -= 25
    if data['compost_safe'].lower() != "yes":
        score -= 15
    return max(score, 0)
