# 🌿 GreenMeds – Medicine Environmental Impact Detector

GreenMeds is a deployable Streamlit web application that helps users identify the environmental toxicity and safe disposal recommendations of medicines, based on either direct selection or text extraction from pill label images. It uses OCR (Optical Character Recognition), fuzzy matching, and an internal database to assess the eco-score of the medicine.

---

## 🚀 Features

- 🔍 **Two Input Modes**: Choose medicine from a dropdown OR upload a pill label image.
- 📷 **OCR Support**: Automatically detects medicine name from uploaded image using Tesseract.
- 🤖 **Fuzzy Matching**: If no exact match is found, the app suggests similar medicine names.
- 🌱 **Eco Toxicity Score**: Computes a score out of 100 based on toxicity and compost safety.
- ♻️ **Disposal Guidance**: Informs users about safe disposal and compost compatibility.
- 📄 **Downloadable PDF Report**: Generates a neat eco-impact report for the selected medicine.
- 🧪 **Explore Database**: Filter and view all medicine data based on toxicity level.

---

## 📁 Project Structure

greenmeds_app/
├── app.py
├── requirements.txt
├── README.md
├── data/
│ └── meds_info.csv
├── utils/
│ ├── ocr.py
│ ├── scores.py
│ └── fuzzy_match.py

yaml
Copy code

---

## 🖥️ Running the App Locally

### ✅ Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/greenmeds_app.git
cd greenmeds_app
✅ Step 2: Set Up Virtual Environment (Optional but Recommended)
bash
Copy code
python -m venv venv
venv\Scripts\activate  # Windows
✅ Step 3: Install Requirements
bash
Copy code
pip install -r requirements.txt
✅ Step 4: Install Tesseract OCR
Download and install from Tesseract GitHub.

After installation, add the installed path (e.g., C:\Program Files\Tesseract-OCR) to your System Environment Variables → PATH.

✅ Step 5: Run the App
bash
Copy code
streamlit run app.py
📦 Dataset Format (data/meds_info.csv)
Your CSV should contain the following columns:

medicine	toxicity_level	compost_safe	disposal	warnings
Ibuprofen	Medium	No	Do not flush, use takeback	Harmful to aquatic organisms
Paracetamol	Low	Yes	Dispose in regular trash	None
Prednisone XL	High	No	Hazardous waste facility	Extremely toxic, handle with care

🧠 Technologies Used
Streamlit – for building the web UI

Pandas – for dataset handling

Pytesseract – for OCR text extraction

Fuzzywuzzy/difflib – for medicine name matching

ReportLab – for generating PDF reports

🧪 Sample Use Cases
A user uploads an image of a pill label. OCR extracts the name Ibuprofen.

The app looks up Ibuprofen in the dataset.

If found, it shows:

✅ Eco score

✅ Warnings

✅ Compost compatibility

✅ Disposal method

✅ PDF download button

If not found, it provides close fuzzy matches like Ibuprofen 400mg, IbuProfen, etc.

✅ To-Do / Future Enhancements
🔍 Use a larger, real-world medicine dataset

📱 Make the app mobile-friendly

🌐 Add multilingual OCR (Hindi, Tamil, etc.)

📊 Add graphical eco-impact comparisons

📜 License
This project is built for learning and educational purposes only. Feel free to fork and improve.

🙋‍♀️ Author
Anushree Kadwadkar
Final Year – B.E. Computer Science
Passionate about real-world AI for sustainability and healthcare.