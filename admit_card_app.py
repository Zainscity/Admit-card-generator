import os
import io
import json
import base64
import requests
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageOps
import streamlit as st

# ---------- FONT SETUP ----------
FONT_DIR = os.path.join(os.path.dirname(__file__), "fonts")
def load_font(filename, size):
    path = os.path.join(FONT_DIR, filename)
    if not os.path.isfile(path):
        st.error(f"Font not found: {path}")
        st.stop()
    return ImageFont.truetype(path, size)

try:
    font_heading = load_font("roboto.ttf", 34)
    font_section = load_font("robotobold.ttf", 24)
    font_regular = load_font("roboto.ttf", 22)
    font_bold = load_font("robotobold.ttf", 22)
    font_note = load_font("roboto.ttf", 20)
    font_signature = load_font("roboto.ttf", 18)
except Exception as e:
    st.exception(e)

# ---------- STREAMLIT UI ----------
st.set_page_config(page_title="Admit Card Generator", layout="wide")
st.markdown("<h1 style='text-align: center;'>Admit Card Generator</h1>", unsafe_allow_html=True)
st.markdown("---")

with st.form("admit_form", clear_on_submit=False):
    st.subheader("Enter Candidate Details")
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Student Name")
        father_name = st.text_input("Father's Name")
        programme = st.selectbox("Programme", ["BSN", "Btech", "Mtech", "Other"])
        cnic = st.text_input("CNIC / B.Form No", max_chars=15)

    with col2:
        admit_card_no = st.text_input("Admit Card No", max_chars=10)
        phone = st.text_input("Phone No.", max_chars=15)

    uploaded_image = st.file_uploader("Upload Passport Size Photo", type=["jpg", "jpeg", "png"])
    submitted = st.form_submit_button("✨ Generate Admit Card")

# ---------- GOOGLE DRIVE UPLOAD ----------
def upload_to_drive(img_bytes, metadata_dict, web_app_url):
    base64_image = base64.b64encode(img_bytes).decode('utf-8')
    payload = {
        "image": base64_image,
        "metadata": json.dumps(metadata_dict)
    }
    try:
        response = requests.post(web_app_url, data=payload)
        return response.text
    except Exception as e:
        return f"❌ Failed to upload: {e}"

# ---------- ADMIT CARD GENERATION ----------
if submitted:
    if not all([name, father_name, programme, cnic, admit_card_no, uploaded_image]):
        st.error("Please fill all fields and upload a photo.")
    elif not admit_card_no.isdigit():
        st.error("Admit Card No must be numeric.")
    else:
        width, height = 1200, 1100
        card = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(card)

        # Header
        draw.rectangle((0, 0, width, 90), fill="#e8f0fe")
        heading_text = "ADMIT CARD"
        heading_bbox = draw.textbbox((0, 0), heading_text, font=font_heading)
        draw.text(((width - heading_bbox[2]) // 2, 22), heading_text, font=font_heading, fill="#1a237e")

        # Photo
        user_img = Image.open(uploaded_image).resize((160, 200))
        user_img = ImageOps.expand(user_img, border=2, fill="#444")
        card.paste(user_img, (980, 105))

        # Info positions
        x_label, x_value = 60, 280
        y, y_gap = 105, 40

        def draw_row(y_pos, label, value):
            draw.text((x_label, y_pos), label, font=font_regular, fill="black")
            draw.text((x_value, y_pos), value, font=font_bold, fill="black")
            return y_pos + y_gap

        y = draw_row(y, "Admit Card No.", admit_card_no)
        y = draw_row(y, "Test Date", "22 July 2024")
        y = draw_row(y, "Test Time", "2:00 PM")
        y = draw_row(y, "Candidate Name", name.title())
        y = draw_row(y, "Father's Name", father_name.title())
        y = draw_row(y, "Programme", programme)
        y = draw_row(y, "CNIC / B.Form", cnic)
        y = draw_row(y, "Phone No.", phone if phone else "N/A")

        # Test Centre
        y += 20
        draw.line(((x_label, y), (width - 60, y)), fill="#ccc", width=1)
        y += 15
        draw.text((x_label, y), "Test Centre", font=font_section, fill="black")
        y += 35
        draw.text((x_label + 20, y), "Mominabad General Hospital", font=font_bold, fill="black")

        # Notes
        y += 55
        draw.line(((x_label, y), (width - 60, y)), fill="#ccc", width=1)
        y += 15
        draw.text((x_label, y), "Instructions", font=font_section, fill="black")
        y += 30
        notes = [
            "Arrive 30 minutes before the test.",
            "Bring your Admit Card and original CNIC/B-Form.",
            "Mobile phones and gadgets are not allowed.",
            "No entry after the test starts."
        ]
        for note in notes:
            draw.text((x_label + 20, y), f"• {note}", font=font_note, fill="black")
            y += 30

        # Signature Line
        y += 30
        sig_x_start = width - 370
        sig_x_end = width - 80
        sig_y = y + 30
        draw.line((sig_x_start, sig_y, sig_x_end, sig_y), fill="black", width=2)
        draw.text((sig_x_start, sig_y + 10), "Authorized Signature", font=font_signature, fill="black")

        # Display card
        st.markdown("---")
        st.subheader("📎 Admit Card Preview")
        buf = io.BytesIO()
        card.save(buf, format="PNG")
        st.image(buf.getvalue(), use_container_width=True)

        # Download button
        st.download_button("⬇️ Download Admit Card", data=buf.getvalue(),
                           file_name=f"AdmitCard_{name.replace(' ', '_')}.png", mime="image/png")

        # Upload to Google Drive
        metadata = {
            "name": name,
            "father_name": father_name,
            "admit_card_no": admit_card_no,
            "programme": programme,
            "cnic": cnic,
            "phone": phone,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        web_app_url = "https://script.google.com/macros/s/AKfycbxGzFULRg-UPvI3KpV-AX_OZVAw81MKdg3Hrb-B7Ni9dL6wTKWk9G9jJWl6YeHBg6zxNA/exec"  # Replace with your URL
        result = upload_to_drive(buf.getvalue(), metadata, web_app_url)
        st.success(result)
