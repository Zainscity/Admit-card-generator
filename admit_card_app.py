import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import datetime
import io

st.set_page_config(page_title="Admit Card Generator", layout="centered")

# Title
st.title("🎓 Admit Card Generator")

# User Input
st.subheader("Fill out the form below to generate your Admit Card")

name = st.text_input("Full Name")
father_name = st.text_input("Father's Name")
admit_card_no = st.number_input("Admit Card No.", min_value=0, format="%d")
test_password = st.text_input("Test Password", value="AirUniversity12!")
program = st.text_input("Programme", value="Bachelor of Science in Computer Sciences")
block = st.text_input("Block", value="IAA-UG")

# Predefined classes
classes = ["9th", "10th", "11th", "12th"]
selected_class = st.selectbox("Class", classes)

# Date and Time pickers
test_date = st.date_input("Test Date", value=datetime.date.today())
test_time = st.time_input("Test Time", value=datetime.time(hour=14, minute=0))

# Upload picture
image_file = st.file_uploader("Upload Passport Size Image", type=["jpg", "jpeg", "png"])

st.markdown("---")

# Generate Card Function
def generate_admit_card():
    # Create base image
    card = Image.new("RGB", (1000, 700), "white")
    draw = ImageDraw.Draw(card)

    # Fonts
    font_path = "arial.ttf"  # Adjust if deploying
    try:
        font_bold = ImageFont.truetype(font_path, 26)
        font_regular = ImageFont.truetype(font_path, 22)
        font_header = ImageFont.truetype(font_path, 30)
        font_center = ImageFont.truetype(font_path, 28)
    except:
        font_bold = ImageFont.load_default()
        font_regular = ImageFont.load_default()
        font_header = ImageFont.load_default()
        font_center = ImageFont.load_default()

    # Header
    draw.text((30, 30), "Reference No. 191337", font=font_regular, fill="black")
    draw.text((420, 30), "ADMIT CARD", font=font_header, fill="black")

    # Center line
    center_text = "Admit Card For Admission Test"
    bbox = draw.textbbox((0, 0), center_text, font=font_center)
    text_width = bbox[2] - bbox[0]
    x_center = (1000 - text_width) // 2
    draw.text((x_center, 70), center_text, font=font_center, fill="black")

    # Main info
    draw.text((30, 130), f"Admit Card No. {int(admit_card_no)}", font=font_regular, fill="black")
    draw.text((500, 130), "Test Password: " + test_password, font=font_regular, fill="black")

    draw.text((30, 180), f"Name: ", font=font_regular, fill="black")
    draw.text((160, 180), name, font=font_bold, fill="black")

    draw.text((30, 220), f"Father's Name: ", font=font_regular, fill="black")
    draw.text((250, 220), father_name, font=font_bold, fill="black")

    draw.text((30, 260), f"Programme: ", font=font_regular, fill="black")
    draw.text((250, 260), program, font=font_regular, fill="black")

    draw.text((30, 300), f"Class: ", font=font_regular, fill="black")
    draw.text((250, 300), selected_class, font=font_regular, fill="black")

    # Right side: date/time/block
    draw.text((600, 180), "Test Date", font=font_regular, fill="black")
    draw.text((750, 180), test_date.strftime("%B %d, %Y - %A"), font=font_regular, fill="black")

    draw.text((600, 220), "Test Timing", font=font_regular, fill="black")
    draw.text((750, 220), test_time.strftime("%I:%M %p").lower(), font=font_regular, fill="black")

    draw.text((600, 260), "Block", font=font_regular, fill="black")
    draw.text((750, 260), block, font=font_regular, fill="black")

    # Image on right
    if image_file:
        user_img = Image.open(image_file).resize((180, 220))
        card.paste(user_img, (780, 320))

    # Admission Test Center
    draw.text((30, 370), "ADMISSION TEST CENTRE", font=font_bold, fill="black")
    draw.text((30, 400), "Air University, Sector E-9, Islamabad.", font=font_regular, fill="black")

    # Notes
    draw.text((30, 460), "NOTE:", font=font_bold, fill="black")
    notes = [
        "• Please be seated half an hour before start of test.",
        "• Please bring lead pencil, ballpoint pen, your Admit Card and CNIC / B Form on test day.",
        "• Calculators, Mobile or any supporting electronic gadget are not allowed in the examination hall.",
        "• No entry shall be allowed after start of the test.",
        "• Parking inside the campus is not allowed. Please make pick and drop arrangements accordingly.",
    ]
    y = 490
    for note in notes:
        draw.text((40, y), note, font=font_regular, fill="black")
        y += 30

    return card

# Button and Display
if st.button("Generate Admit Card"):
    if name and father_name and image_file:
        card_img = generate_admit_card()
        st.image(card_img, caption="Admit Card Preview", use_container_width=True)

        # Download Button
        img_byte_arr = io.BytesIO()
        card_img.save(img_byte_arr, format='PNG')
        st.download_button("📥 Download Admit Card", data=img_byte_arr.getvalue(),
                           file_name="admit_card.png", mime="image/png")
    else:
        st.error("Please fill in all fields and upload a picture.")
