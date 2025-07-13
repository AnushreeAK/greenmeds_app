import pytesseract
from PIL import Image
import re
import tempfile

def extract_text_from_image(uploaded_file):
    # Save uploaded image temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_path = temp_file.name

    try:
        # Run OCR using pytesseract
        image = Image.open(temp_path)
        raw_text = pytesseract.image_to_string(image)

        # Clean and extract potential medicine-like words (words with alphabets and numbers)
        lines = raw_text.splitlines()
        medicine_candidates = []

        for line in lines:
            line = line.strip()
            if re.search(r'[A-Za-z]{3,}', line):  # Has at least 3 letters
                medicine_candidates.append(line)

        # Choose the longest candidate line (assuming it's most relevant)
        if medicine_candidates:
            best_guess = max(medicine_candidates, key=len)
        else:
            best_guess = "No medicine name found"

        return best_guess.strip()

    except Exception as e:
        return f"OCR Error: {str(e)}"
