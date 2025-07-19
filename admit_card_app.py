import os
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
from datetime import datetime


# Set up font loading
FONT_DIR = os.path.join(os.path.dirname(__file__), "fonts")

def load_font(filename, size):
    """Loads a font file from the 'fonts' directory."""
    path = os.path.join(FONT_DIR, filename)
    if not os.path.isfile(path):
        # Provide a helpful error if fonts are missing
        st.error(f"❌ Font file not found at {path}. Please create a 'fonts' folder and add 'arial.ttf' and 'arialbd.ttf'.")
        st.stop()
    return ImageFont.truetype(path, size)

# Load fonts with sizes appropriate for the new design
try:
    font_heading = load_font("arialbd.ttf", 34)
    font_section_heading = load_font("arialbd.ttf", 24)
    font_regular = load_font("arial.ttf", 22)
    font_bold = load_font("arialbd.ttf", 22)
    font_note = load_font("arial.ttf", 20)
except Exception as e:
    st.exception(e)


st.set_page_config(page_title="Admit Card Generator", layout="wide")
st.markdown("<h1 style='text-align: center;'>Admit Card Generator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>This tool generates a simplified version of the admit card.</p>", unsafe_allow_html=True)
st.markdown("---")

# --- Input Form (Functionality Unchanged) ---
with st.form("admit_form", clear_on_submit=False):
    st.subheader("Enter Candidate Details")
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Student Name")
        father_name = st.text_input("Father's Name", "Father's Name")
        programme = st.text_input("Programme", "Bachelor Of Science In Computer Sciences")
        class_name = st.selectbox("Class (Not used in this design)", ["9th", "10th", "11th", "12th"])
        cnic = st.text_input("CNIC / B.Form No (Not used)", help="Numeric only", max_chars=15)
        
    with col2:
        admit_card_no = st.text_input("Admit Card No", "*******", help="Numeric only", max_chars=10)
        test_password = st.text_input("Test Password", "Password")
        test_date = st.date_input("Test Date", datetime(2024, 7, 22))
        test_time = st.time_input("Test Time", datetime.strptime("02:00 PM", "%I:%M %p").time())
        phone = st.text_input("Phone No. (Not used)", help="Numeric only", max_chars=15)

    uploaded_image = st.file_uploader("Upload Passport Size Photo (Required)", type=["jpg", "jpeg", "png"])
    submitted = st.form_submit_button("✨ Generate Admit Card")

# --- Image Generation (Visuals Replicated) ---
if submitted:
    # Validation for fields used in the card
    required_fields = [name, father_name, programme, admit_card_no, test_password]
    if not all(required_fields):
        st.error("Please fill all required fields: Name, Father's Name, Programme, Admit Card No, and Test Password.")
    elif not admit_card_no.isdigit():
        st.error("Admit Card No must be numeric.")
    elif not uploaded_image:
        st.error("Please upload your passport size photo.")
    else:
        # --- Card Generation Logic ---
        card_width, card_height = 1200, 850 # Adjusted height for fewer fields
        card = Image.new("RGB", (card_width, card_height), "white")
        draw = ImageDraw.Draw(card)

        # Hardcoded values from the sample image
        centre_details = "Mominabad General Hospital."
        notes_list = [
            "Please be seated half an hour before start of test.",
            "Please bring lead pencil, ballpoint pen, your Admit Card and CNIC / B Form on test day.",
            "Calculators, Mobile or any supporting electronic gadget are not allowed in the examination hall.",
            "No entry shall be allowed after start of the test.",
            "Parking inside the campus is not allowed. Please make pick and drop arrangements, accordingly."
        ]
        
        # Format date and time to match the sample
        test_date_str = test_date.strftime('%B %d, %Y - %A').upper()
        test_time_str = test_time.strftime('%I:%M %p').lower()

        # 1. Header and Title
        draw.rectangle((0, 0, card_width, 80), fill="#F0F0F0")
        draw.line(((0, 80), (card_width, 80)), fill="#CCCCCC", width=2)
        heading_text = "ADMIT CARD"
        heading_bbox = draw.textbbox((0, 0), heading_text, font=font_heading)
        draw.text(((card_width - heading_bbox[2]) / 2, (80 - heading_bbox[3]) / 2), heading_text, font=font_heading, fill="black")

        # 2. Photo
        user_img = Image.open(uploaded_image).resize((180, 220))
        photo_x, photo_y = 980, 110
        card.paste(user_img, (photo_x, photo_y))
        draw.rectangle((photo_x - 1, photo_y - 1, photo_x + 180, photo_y + 220), outline="#AAAAAA")

        # 3. Main Details Section (Layout updated to remove fields)
        y = 120
        y_gap = 55
        x_label1, x_value1 = 40, 240
        x_label2, x_value2 = 520, 690

        # Row 1: Admit Card No | Test Date
        draw.text((x_label1, y), "Admit Card No.", font=font_regular, fill="black")
        draw.text((x_value1, y), admit_card_no, font=font_bold, fill="black")
        draw.text((x_label2, y), "Test Date", font=font_regular, fill="black")
        draw.text((x_value2, y), test_date_str, font=font_bold, fill="black")
        
        # Row 2: Test Password | Test Timing
        y += y_gap
        draw.text((x_label1, y), "Test Password:", font=font_regular, fill="black")
        draw.text((x_value1, y), test_password, font=font_bold, fill="black")
        draw.text((x_label2, y), "Test Timing", font=font_regular, fill="black")
        draw.text((x_value2, y), test_time_str, font=font_bold, fill="black")

        # Rows 3-5: Single column fields
        y += y_gap * 1.5 # Extra space before full-width fields
        draw.text((x_label1, y), "Name", font=font_regular, fill="black")
        draw.text((x_value1, y), name.title(), font=font_bold, fill="black")
        
        y += y_gap
        draw.text((x_label1, y), "Father's Name", font=font_regular, fill="black")
        draw.text((x_value1, y), father_name.title(), font=font_bold, fill="black")

        y += y_gap
        draw.text((x_label1, y), "Programme", font=font_regular, fill="black")
        draw.text((x_value1, y), programme, font=font_bold, fill="black")

        # 4. Admission Test Centre Section
        y += y_gap * 1.2
        draw.line(((x_label1, y), (card_width - 40, y)), fill="#DDDDDD", width=1)
        y += 20
        draw.text((x_label1, y), "ADMISSION TEST CENTRE", font=font_section_heading, fill="black")
        y += 40
        draw.text((x_label1 + 40, y), centre_details, font=font_bold, fill="black")

        # 5. Note Section
        y += y_gap * 1.2
        draw.line(((x_label1, y), (card_width - 40, y)), fill="#DDDDDD", width=1)
        y += 20
        draw.text((x_label1, y), "NOTE:", font=font_section_heading, fill="black")
        y += 25
        note_gap = 35
        for note in notes_list:
            y += note_gap
            draw.text((x_label1 + 20, y), "•", font=font_bold, fill="black")
            draw.text((x_label1 + 45, y), note, font=font_note, fill="black")

        # --- Display and Download ---
        st.markdown("---")
        st.subheader("Generated Admit Card Preview")
        buffer = io.BytesIO()
        card.save(buffer, format="PNG")
        st.image(buffer.getvalue(), use_container_width=True)
        st.download_button(
            label="⬇️ Download Admit Card",
            data=buffer.getvalue(),
            file_name=f"AdmitCard_{name.replace(' ', '_')}.png",
            mime="image/png"
        )