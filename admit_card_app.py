import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
from datetime import datetime

# Title and Page Settings
st.set_page_config(page_title="Admit Card Generator", layout="centered")

st.markdown("<h1 style='text-align: center;'>Admit Card Generator</h1>", unsafe_allow_html=True)
st.markdown("---")

# Form
with st.form("admit_form", clear_on_submit=False):
    col1, col2 = st.columns([3, 1])

    with col1:
        name = st.text_input("Student Name")
        father_name = st.text_input("Father's Name")
        programme = st.text_input("Programme", placeholder="e.g. Bachelor of Science in Computer Sciences")
        class_name = st.selectbox("Class", ["9th", "10th", "11th", "12th"])
        block = st.text_input("Block")
        admit_card_no = st.text_input("Admit Card No", help="Only numeric values allowed", max_chars=10)
        test_password = st.text_input("Test Password")
        test_date = st.date_input("Test Date")
        test_time = st.time_input("Test Time")

    with col2:
        uploaded_image = st.file_uploader("Upload Passport Size Photo", type=["jpg", "jpeg", "png"])

    submitted = st.form_submit_button("Generate Admit Card")

# Font paths (replace with your own if required)
font_bold = "arialbd.ttf"
font_regular = "arial.ttf"

if submitted:
    if not all([name, father_name, programme, block, admit_card_no, test_password]):
        st.error("Please fill all fields.")
    elif not admit_card_no.isdigit():
        st.error("Admit Card No must be numeric only.")
    elif not uploaded_image:
        st.error("Please upload an image.")
    else:
        # Load base canvas
        card_width, card_height = 1000, 600
        card = Image.new("RGB", (card_width, card_height), "white")
        draw = ImageDraw.Draw(card)

        # Load fonts
        try:
            bold = ImageFont.truetype(font_bold, 20)
            big_bold = ImageFont.truetype(font_bold, 28)
            regular = ImageFont.truetype(font_regular, 18)
            small = ImageFont.truetype(font_regular, 14)
        except:
            bold = big_bold = regular = small = ImageFont.load_default()

        # Draw border
        border_color = "#2784f2"
        border_width = 8
        draw.rectangle([0, 0, card_width - 1, card_height - 1], outline=border_color, width=border_width)

        # Admit Card Heading
        heading = "ADMIT CARD"
        w, _ = draw.textbbox((0, 0), heading, font=big_bold)[2:]
        draw.text(((card_width - w) // 2, 30), heading, font=big_bold, fill="black")

        # Photo
        user_img = Image.open(uploaded_image).resize((150, 180))
        card.paste(user_img, (card_width - 200, 100))

        # Static + dynamic text blocks
        x_left = 50
        y_start = 90
        spacing = 40

        draw.text((x_left, y_start), f"Admit Card No: {admit_card_no}", font=bold, fill="black")
        draw.text((x_left, y_start + spacing), f"Test Password: {test_password}", font=regular, fill="black")

        draw.text((x_left, y_start + spacing * 2), f"Name: {name}", font=regular, fill="black")
        draw.text((x_left + 500, y_start + spacing * 2), f"Test Date: {test_date.strftime('%B %d, %Y')}", font=regular, fill="black")

        draw.text((x_left, y_start + spacing * 3), f"Father's Name: {father_name}", font=regular, fill="black")
        draw.text((x_left + 500, y_start + spacing * 3), f"Test Timing: {test_time.strftime('%I:%M %p')}", font=regular, fill="black")

        draw.text((x_left, y_start + spacing * 4), f"Programme: {programme}", font=regular, fill="black")
        draw.text((x_left + 500, y_start + spacing * 4), f"Block: {block}", font=regular, fill="black")

        draw.text((x_left, y_start + spacing * 5), f"Class: {class_name}", font=regular, fill="black")

        # Centre Info
        y_centre = y_start + spacing * 7
        draw.text((x_left, y_centre), "ADMISSION TEST CENTRE", font=bold, fill="black")
        draw.text((x_left, y_centre + 25), "Air University, Sector E-9, Islamabad.", font=regular, fill="black")

        # Notes
        y_note = y_centre + 70
        draw.text((x_left, y_note), "NOTE:", font=bold, fill="black")
        notes = [
            "➤ Please be seated half an hour before start of test.",
            "➤ Bring pencil, pen, Admit Card, and CNIC / B Form.",
            "➤ Electronic gadgets are not allowed.",
            "➤ No entry after test start time.",
            "➤ Parking is not allowed. Arrange drop-off accordingly.",
        ]
        for i, note in enumerate(notes):
            draw.text((x_left + 10, y_note + 25 + i * 25), note, font=small, fill="black")

        # Save to buffer
        buf = io.BytesIO()
        card.save(buf, format="PNG")
        st.image(buf.getvalue(), caption="Generated Admit Card", use_container_width=True)

        # Download
        st.download_button("Download Admit Card", buf.getvalue(), file_name="admit_card.png", mime="image/png")
