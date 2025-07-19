import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
from datetime import date
import datetime

# --- Streamlit App Setup ---
st.set_page_config(page_title="Admit Card Generator", layout="centered")

st.markdown("""
    <style>
        .stButton>button {
            background-color: #4A90E2;
            color: white;
            font-weight: bold;
            border-radius: 10px;
            padding: 0.5rem 1rem;
        }
        .stDownloadButton>button {
            background-color: #2ECC71;
            color: white;
            font-weight: bold;
            border-radius: 10px;
            padding: 0.5rem 1rem;
        }
        .stTextInput>div>input, .stSelectbox>div, .stDateInput>div>input, .stTimeInput>div>input {
            border-radius: 6px;
            border: 1px solid #ccc;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #4A90E2;'>📄 Admit Card Generator</h1>", unsafe_allow_html=True)
st.markdown("---")

# --- Input Fields Layout ---
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        admit_no = st.number_input("🎫 Admit Card No.", min_value=0, step=1, format="%d")
        name = st.text_input("👤 Name")
        father_name = st.text_input("👨‍👧 Father's Name")
        program = st.selectbox("📘 Programme", ['Science', 'Commerce'])

    with col2:
        test_password = st.text_input("🔐 Test Password")
        test_class = st.selectbox("🏫 Class", ['9th', '10th', '11th', '12th'])
        test_date = st.date_input("🗓️ Test Date", value=date.today())
        test_time = st.time_input("⏰ Test Time", value=datetime.time(14, 0))

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

    # Centered line
    center_text = "Admit Card For Admission Test"
    bbox = draw.textbbox((0, 0), center_text, font=font)
    text_width = bbox[2] - bbox[0]
    center_x = (1000 - text_width) // 2
    draw.text((center_x, 120), center_text, font=font, fill="black")

    draw.text((40, 160), f"Test Password: {test_password}", font=font, fill="black")

    # Personal Info
    draw.text((40, 200), f"Name: {name}", font=font_bold, fill="black")
    draw.text((500, 200), f"Test Date: {test_date.strftime('%B %d, %Y')}", font=font, fill="black")
    draw.text((40, 240), f"Father's Name: {father_name}", font=font_bold, fill="black")
    draw.text((500, 240), f"Test Timing: {test_time.strftime('%I:%M %p')}", font=font, fill="black")
    draw.text((40, 280), f"Programme: {program}", font=font, fill="black")
    draw.text((500, 280), f"Block: {block}", font=font, fill="black")
    draw.text((40, 320), f"Class: {test_class}", font=font, fill="black")

    # Test Centre
    draw.text((40, 370), "ADMISSION TEST CENTRE", font=font_bold, fill="#000000")
    draw.text((40, 400), test_centre, font=font, fill="black")

    # Notes
    draw.text((40, 440), "NOTE:", font=font_bold, fill="#000000")
    notes = [
        "Please be seated half an hour before start of test.",
        "Bring pencil, pen, Admit Card, and CNIC / B Form.",
        "Electronic gadgets are not allowed.",
        "No entry after test start time.",
        "Parking is not allowed. Arrange drop-off accordingly."
    ]
    y = 470
    for note in notes:
        draw.text((60, y), f"• {note}", font=font_small, fill="black")
        y += 25

    # Passport Photo
    if passport_photo:
        img = Image.open(passport_photo).resize((150, 180))
        card.paste(img, (800, 120))

    return card

# --- Generate Button ---
st.markdown("###")
col_gen, col_blank, col_print = st.columns([1, 2, 1])
with col_gen:
    if st.button("🛠️ Generate Admit Card"):
        if all([admit_no, test_password, name, father_name, program, test_time, block, test_centre, passport_photo]):
            card = generate_card()

            st.image(card, caption="🖨️ Preview: Admit Card", use_container_width=True)

            buf = io.BytesIO()
            card.save(buf, format="PNG")
            byte_im = buf.getvalue()

            # Download Button
            st.download_button("📥 Download Admit Card", data=byte_im, file_name="admit_card.png", mime="image/png")

            # Print Button (opens print dialog)
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
            st.error("⚠️ Please fill in all the fields and upload a passport photo.")
