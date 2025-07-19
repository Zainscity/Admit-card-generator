import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
from datetime import date
import datetime


# --- Streamlit App Setup ---
st.set_page_config(page_title="Admit Card Generator", layout="centered")

st.markdown("<h1 style='text-align: center; color: #4A90E2;'>📄 Admit Card Generator</h1>", unsafe_allow_html=True)
st.markdown("---")

# --- Input Fields Layout ---
col1, col2 = st.columns(2)
with col1:
    admit_no = st.number_input("🎫 Admit Card No.", min_value=0, step=1, format="%d")
    name = st.text_input("👤 Name")
    father_name = st.text_input("👨‍👧 Father's Name")
    program = st.selectbox("📘 Programme",[ 'Science', 'Commerce'] )

with col2:
    test_password = st.text_input("🔐 Test Password")
    test_class = st.selectbox("🏫 Class", ['9th', '10th', '11th', '12th'])
    test_date = st.date_input("🗓️ Test Date", value=date.today())
    test_time = st.time_input("⏰ Test Time", value=datetime.time(14, 0))  # default 2:00 PM

block = st.text_input("🏢 Block (e.g., IAA-UG)")
test_centre = st.text_input("📍 Test Centre", value="Air University, Sector E-9, Islamabad.")
passport_photo = st.file_uploader("🖼️ Upload Passport Size Photo", type=['jpg', 'jpeg', 'png'])

# --- Card Generator ---
def generate_card():
    card = Image.new("RGB", (1000, 600), "white")
    draw = ImageDraw.Draw(card)

    # Fonts
    try:
        font_bold = ImageFont.truetype("arialbd.ttf", 24)
        font = ImageFont.truetype("arial.ttf", 22)
        font_small = ImageFont.truetype("arial.ttf", 18)
    except:
        font_bold = font = font_small = ImageFont.load_default()

    # Header
    draw.rectangle([10, 10, 990, 590], outline="#4A90E2", width=3)
    draw.text((400, 30), "ADMIT CARD", font=font_bold, fill="#000000")
    draw.text((40, 80), f"Admit Card No: {admit_no}", font=font, fill="black")
    draw.text((500, 80), "Admit Card For Admission Test", font=font, fill="black")
    draw.text((40, 120), f"Test Password: {test_password}", font=font, fill="black")

    # Personal info
    draw.text((40, 170), f"Name: {name}", font=font_bold, fill="black")
    draw.text((500, 170), f"Test Date: {test_date.strftime('%B %d, %Y')}", font=font, fill="black")
    draw.text((40, 210), f"Father's Name: {father_name}", font=font_bold, fill="black")
    draw.text((500, 210), f"Test Timing: {test_time.strftime('%I:%M %p')}", font=font, fill="black")
    draw.text((40, 250), f"Programme: {program}", font=font, fill="black")
    draw.text((500, 250), f"Block: {block}", font=font, fill="black")
    draw.text((40, 290), f"Class: {test_class}", font=font, fill="black")

    # Test Centre
    draw.text((40, 340), "ADMISSION TEST CENTRE", font=font_bold, fill="#000000")
    draw.text((40, 370), test_centre, font=font, fill="black")

    # Notes
    draw.text((40, 410), "NOTE:", font=font_bold, fill="#000000")
    notes = [
        "Please be seated half an hour before start of test.",
        "Bring pencil, pen, Admit Card, and CNIC / B Form.",
        "Electronic gadgets are not allowed.",
        "No entry after test start time.",
        "Parking is not allowed. Arrange drop-off accordingly."
    ]
    y = 440
    for note in notes:
        draw.text((60, y), f"• {note}", font=font_small, fill="black")
        y += 25

    # Passport image
    if passport_photo:
        img = Image.open(passport_photo).resize((150, 180))
        card.paste(img, (800, 120))

    return card

# --- Generate Card Button ---
if st.button("🛠️ Generate Admit Card"):
    if all([admit_no, test_password, name, father_name, program, test_time, block, test_centre, passport_photo]):
        card = generate_card()

        st.image(card, caption="Admit Card Preview", use_container_width=True)

        buf = io.BytesIO()
        card.save(buf, format="PNG")
        byte_im = buf.getvalue()

        # Download
        st.download_button("📥 Download Admit Card", data=byte_im, file_name="admit_card.png", mime="image/png")

        # Print
        st.components.v1.html(f"""
        <script>
        const image = new Image();
        image.src = "data:image/png;base64,{byte_im.hex()}";
        image.onload = () => {{
            const w = window.open('');
            w.document.write('<img src="' + image.src + '" onload="window.print(); window.close();" />');
        }};
        </script>
        """, height=0)
    else:
        st.error("Please fill in all the fields and upload a photo.")
