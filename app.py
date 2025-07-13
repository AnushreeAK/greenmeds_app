import streamlit as st
import pandas as pd
from utils.scores import get_medicine_data, calculate_eco_score
from utils.ocr import extract_text_from_image
from io import BytesIO
from reportlab.pdfgen import canvas

# Load dataset
df = pd.read_csv("data/meds_info.csv")
medicine_list = sorted(df['medicine'].tolist())

# Streamlit page config
st.set_page_config(page_title="GreenMeds – Eco Impact Detector", page_icon="🌿")

# Header
st.markdown("<h1 style='color:green;'>🌿 GreenMeds</h1>", unsafe_allow_html=True)
st.markdown("**A Medicine Environmental Impact Detector for a Greener Planet 🌏**")
st.image("https://cdn-icons-png.flaticon.com/512/2917/2917994.png", width=100)

# Sidebar
st.sidebar.header("🔍 Check Medicine Impact")
input_method = st.sidebar.radio("Choose Input Method:", ["Select from List", "Upload Image"])

# Input handling
med_name = ""
if input_method == "Select from List":
    med_name = st.sidebar.selectbox("Choose Medicine", options=medicine_list)
elif input_method == "Upload Image":
    uploaded_file = st.sidebar.file_uploader("Upload Pill Label Image", type=["jpg", "png"])
    if uploaded_file:
        med_name = extract_text_from_image(uploaded_file)
        st.sidebar.success(f"Detected Medicine: {med_name}")
        st.sidebar.write("📃 Raw Extracted Text:")
        st.sidebar.code(med_name)

# PDF generation function
def generate_pdf(data, score):
    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, "GreenMeds - Eco Report")
    c.setFont("Helvetica", 12)
    c.drawString(50, 770, f"Medicine: {data['medicine']}")
    c.drawString(50, 750, f"Eco Toxicity Score: {score}/100")
    c.drawString(50, 730, f"Toxicity Level: {data['toxicity_level']}")
    c.drawString(50, 710, f"Disposal: {data['disposal']}")
    c.drawString(50, 690, f"Compost Safe: {data['compost_safe']}")
    c.drawString(50, 670, f"Warnings: {data['warnings']}")
    c.save()
    buffer.seek(0)
    return buffer

# Main result section
if med_name:
    st.subheader(f"🧾 Results for: **{med_name}**")
    med_data = get_medicine_data(med_name)

    if isinstance(med_data, dict) and "fallback" not in med_data:
        eco_score = calculate_eco_score(med_data)
        st.markdown(f"### 🌱 Eco Toxicity Score: `{eco_score}/100`")
        st.progress(eco_score)

        if med_data['toxicity_level'] == "Low" and med_data['compost_safe'].lower() == "yes":
            st.success("✅ This medicine is considered **eco-safe**!")
        elif med_data['toxicity_level'] == "High":
            st.error("⚠️ This medicine has **high environmental toxicity**.")

        st.markdown(f"**⚠️ Environmental Warnings:**\n- {med_data['warnings']}")
        st.markdown(f"**♻️ Disposal Recommendation:**\n- {med_data['disposal']}")
        st.markdown(f"**🪱 Compost-safe:** `{med_data['compost_safe']}`")

        with st.expander("🌐 Learn More"):
            st.markdown(f"- [WHO Guidelines](https://www.who.int/publications/i/item/9789241509882)")
            st.markdown(f"- Wikipedia: [{med_name}](https://en.wikipedia.org/wiki/{med_name.replace(' ', '_')})")

        st.info("💡 Tip of the Day: Never flush unused medicines unless instructed.")

        pdf_file = generate_pdf(med_data, eco_score)
        st.download_button(
            label="📄 Download Eco Report (PDF)",
            data=pdf_file,
            file_name=f"{med_name}_eco_report.pdf",
            mime="application/pdf"
        )

    elif isinstance(med_data, dict) and "fallback" in med_data:
        st.warning("🔍 Couldn't find an exact match, but here are close suggestions:")
        suggestion = st.selectbox("Did you mean one of these?", med_data["fallback"])
        if suggestion:
            row = df[df["medicine"].str.lower() == suggestion.lower()]
            if not row.empty:
                row = row.iloc[0].to_dict()
                eco_score = calculate_eco_score(row)

                st.markdown(f"### 🌱 Eco Toxicity Score: `{eco_score}/100`")
                st.progress(eco_score)

                if row['toxicity_level'] == "Low" and row['compost_safe'].lower() == "yes":
                    st.success("✅ This medicine is considered **eco-safe**!")
                elif row['toxicity_level'] == "High":
                    st.error("⚠️ This medicine has **high environmental toxicity**.")

                st.markdown(f"**⚠️ Environmental Warnings:**\n- {row['warnings']}")
                st.markdown(f"**♻️ Disposal Recommendation:**\n- {row['disposal']}")
                st.markdown(f"**🪱 Compost-safe:** `{row['compost_safe']}`")

                with st.expander("🌐 Learn More"):
                    st.markdown(f"- [WHO Guidelines](https://www.who.int/publications/i/item/9789241509882)")
                    st.markdown(f"- Wikipedia: [{suggestion}](https://en.wikipedia.org/wiki/{suggestion.replace(' ', '_')})")

                st.info("💡 Tip: Always dispose of medicines safely.")

                pdf_file = generate_pdf(row, eco_score)
                st.download_button(
                    label="📄 Download Eco Report (PDF)",
                    data=pdf_file,
                    file_name=f"{suggestion}_eco_report.pdf",
                    mime="application/pdf"
                )
            else:
                st.error("⚠️ No data found for this suggestion. Please try another one.")
    else:
        st.error("🚫 No medicine match found. Please check the image or try typing the name.")
else:
    st.warning("Enter or upload a medicine to get started.")

# --- Dataset explorer ---
st.markdown("---")
st.markdown("### 🧪 Explore Medicine Database")
filter_type = st.selectbox("Filter by Toxicity Level", ["All", "Low", "Medium", "High"])
filtered_df = df[df["toxicity_level"] == filter_type] if filter_type != "All" else df
st.dataframe(filtered_df[["medicine", "toxicity_level", "disposal", "compost_safe"]])

# Footer
st.markdown("---")
st.caption("Built with ❤️ for a cleaner, healthier Earth")
