import re
from difflib import get_close_matches

# Clean the extracted OCR text
def clean_text(text):
    text = text.lower()
    text = re.sub(r'\d+mg', '', text)  # remove '500mg', '250mg'
    text = re.sub(r'\b(tab|tablet|cap|capsule|oral|sr|xl)\b', '', text)
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)  # remove special chars
    return text.strip()

# Match cleaned text with cleaned dataset entries using fuzzy logic
def get_best_match_from_dataset(ocr_text, medicine_list):
    cleaned_input = clean_text(ocr_text)
    cleaned_dataset = [clean_text(med) for med in medicine_list]
    matches = get_close_matches(cleaned_input, cleaned_dataset, n=1, cutoff=0.5)

    if matches:
        # Return original name from dataset that matches cleaned version
        for original in medicine_list:
            if clean_text(original) == matches[0]:
                return original
    return None
