import os
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
from datetime import datetime

# Set up font loading
FONT_DIR = os.path.join(os.path.dirname(__file__), "fonts")

def load_font(filename, size):
    path = os.path.join(FONT_DIR, filename)
    if not os.path.isfile(path):
        st.error(f"❌ Font file not found: {path}")
        st.stop()
    return ImageFont.truetype(path, size)

# Load fonts
font_regular = load_font("arial.ttf", 24)
font_bold = load_font("arialbd.ttf", 28)
font_heading = load_font("arialbd.ttf", 36)
font_small = load_font("arial.ttf", 20)

st.set_page_config(page_title="Admit Card Generator", layout="centered")
st.markdown("<h1 style='text-align: center;'>Admit Card Generator</h1>", unsafe_allow_html=True)
st.markdown("---")

# Input form
with st.form("admit_form", clear_on_submit=False):
    col1, col2 = st.columns([3, 1])

    with col1:
        name = st.text_input("Student Name")
        father_name = st.text_input("Father's Name")
        programme = st.text_input("Programme", placeholder="e.g. BS Computer Science")
        class_name = st.selectbox("Class", ["9th", "10th", "11th", "12th"])
        admit_card_no = st.text_input("Admit Card No", help="Numeric only", max_chars=10)
        cnic = st.text_input("CNIC / B.Form No", help="Numeric only", max_chars=15)
        phone = st.text_input("Phone No.", help="Numeric only", max_chars=15)
        test_password = st.text_input("Test Password")
        test_date = st.date_input("Test Date")
        test_time = st.time_input("Test Time")

    with col2:
        uploaded_image = st.file_uploader("Upload Passport Size Photo", type=["jpg", "jpeg", "png"])

    submitted = st.form_submit_button("Generate Admit Card")



# Submit handler
if submitted:
    if not all([
        # name, father_name, programme, admit_card_no, test_password, cnic, phone
        ]):
        st.error("Please fill all fields.")
    elif not (admit_card_no.isdigit() and cnic.isdigit() and phone.isdigit()):
        st.error("Admit Card No, CNIC and Phone must be numeric.")
    elif not uploaded_image:
        st.error("Please upload your passport size photo.")
    else:
        # Generate Card Image
        card_width, card_height = 1000, 650
        card = Image.new("RGB", (card_width, card_height), "white")
        draw = ImageDraw.Draw(card)

        # Border
        border_color = "#2784f2"
        border_width = 10
        draw.rectangle([0, 0, card_width - 1, card_height - 1], outline=border_color, width=border_width)

        # Heading
        heading_text = "ADMIT CARD"
        heading_w = draw.textbbox((0, 0), heading_text, font=font_heading)[2]
        draw.text(((card_width - heading_w) // 2, 30), heading_text, font=font_heading, fill="black")

        # Paste photo
        user_img = Image.open(uploaded_image).resize((160, 200))
        card.paste(user_img, (card_width - 220, 100))

        # Main content positions
        x_left = 60
        y_top = 100
        line_gap = 45

        # First block
        draw.text((x_left, y_top), f"Admit Card No: {admit_card_no}", font=font_bold, fill="black")
        draw.text((x_left, y_top + line_gap), f"Test Password: {test_password}", font=font_regular, fill="black")
        draw.text((x_left, y_top + 2*line_gap), f"Name: {name}", font=font_regular, fill="black")
        draw.text((x_left + 430, y_top + 2*line_gap), f"Test Date: {test_date.strftime('%B %d, %Y')}", font=font_regular, fill="black")
        draw.text((x_left, y_top + 3*line_gap), f"Father's Name: {father_name}", font=font_regular, fill="black")
        draw.text((x_left + 430, y_top + 3*line_gap), f"Test Time: {test_time.strftime('%I:%M %p')}", font=font_regular, fill="black")
        draw.text((x_left, y_top + 4*line_gap), f"Programme: {programme}", font=font_regular, fill="black")
        draw.text((x_left + 430, y_top + 4*line_gap), f"Class: {class_name}", font=font_regular, fill="black")
        draw.text((x_left, y_top + 5*line_gap), f"CNIC / B.Form: {cnic}", font=font_regular, fill="black")
        draw.text((x_left + 430, y_top + 5*line_gap), f"Phone: {phone}", font=font_regular, fill="black")

        # Test Centre
        y_centre = y_top + 6*line_gap
        draw.text((x_left, y_centre), "Test Centre:", font=font_bold, fill="black")
        draw.text((x_left + 180, y_centre), "Mominabad General Hospital", font=font_regular, fill="black")

        # Notes
        y_note = y_centre + 50
        draw.text((x_left, y_note), "NOTE:", font=font_bold, fill="black")
        notes = [
            "➤ Arrive 30 minutes before test start time.",
            "➤ Bring pen, pencil, admit card, and CNIC / B.Form.",
            "➤ Mobile phones and smart devices are not allowed.",
            "➤ No entry after test has started.",
            "➤ No parking available. Arrange drop-off.",
        ]
        for i, note in enumerate(notes):
            draw.text((x_left + 10, y_note + 40 + i * 28), note, font=font_regular, fill="black")


        # Footer
        # Display and Download
        buffer = io.BytesIO()
        card.save(buffer, format="PNG")
        st.image(buffer.getvalue(), caption="Generated Admit Card", use_container_width=True)
        st.download_button("Download Admit Card", buffer.getvalue(), file_name="admit_card.png", mime="image/png")


