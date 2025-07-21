import os
import io
import json
import base64
import requests
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageOps
import streamlit as st

# ---------- FONT SETUP (INCREASED SIZES) ----------
FONT_DIR = os.path.join(os.path.dirname(__file__), "fonts")
def load_font(filename, size):
    path = os.path.join(FONT_DIR, filename)
    if not os.path.isfile(path):
        st.error(f"Font not found: {path}")
        st.stop()
    return ImageFont.truetype(path, size)

try:
    # Font sizes have been increased for better print visibility
    font_heading = load_font("roboto.ttf", 38)
    font_section = load_font("robotobold.ttf", 28)
    font_regular = load_font("roboto.ttf", 26)
    font_bold = load_font("robotobold.ttf", 26)
    font_note = load_font("roboto.ttf", 24)
    font_signature = load_font("roboto.ttf", 22)
except Exception as e:
    st.exception(e)

# ---------- STREAMLIT UI ----------
# This part remains unchanged
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
# This part remains unchanged
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

# ---------- ADMIT CARD GENERATION (LARGER TEXT & ADJUSTED SPACING) ----------
if submitted:
    if not all([name, father_name, programme, cnic, admit_card_no, uploaded_image]):
        st.error("Please fill all fields and upload a photo.")
    elif not admit_card_no.isdigit():
        st.error("Admit Card No must be numeric.")
    else:
        width, height = 1200, 850
        card = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(card)

        # Header
        header_color = "#42a5f5"
        draw.rectangle((0, 0, width, 90), fill=header_color)
        heading_text = "ADMIT CARD"
        heading_bbox = draw.textbbox((0, 0), heading_text, font=font_heading)
        draw.text(((width - heading_bbox[2]) / 2, 20), heading_text, font=font_heading, fill="white")

        # Photo with Border
        user_img = Image.open(uploaded_image).resize((160, 200))
        user_img = ImageOps.expand(user_img, border=3, fill=header_color)
        card.paste(user_img, (980, 105))

        # --- Two-Column Layout for Info ---
        # Increased y_gap for larger fonts
        y_start, y_gap = 110, 48
        y_left_cursor = y_start
        y_right_cursor = y_start

        # Left Column Details
        x_label_left, x_value_left = 60, 300 # Adjusted value start position
        details_left = [
            ("Admit Card No.", admit_card_no),
            ("Candidate Name", name.title()),
            ("Father's Name", father_name.title()),
            ("Programme", programme),
            ("CNIC / B.Form", cnic),
            ("Phone No.", phone if phone else "N/A"),
        ]
        for label, value in details_left:
            draw.text((x_label_left, y_left_cursor), label, font=font_regular, fill="black")
            draw.text((x_value_left, y_left_cursor), value, font=font_bold, fill="black")
            y_left_cursor += y_gap

        # Right Column Details
        x_label_right, x_value_right = 650, 820 # Adjusted value start position
        details_right = [
            ("Test Date", "22 July 2024"),
            ("Test Time", "2:00 PM"),
        ]
        for label, value in details_right:
            draw.text((x_label_right, y_right_cursor), label, font=font_regular, fill="black")
            draw.text((x_value_right, y_right_cursor), value, font=font_bold, fill="black")
            y_right_cursor += y_gap

        # Section Divider
        y = max(y_left_cursor, y_right_cursor)
        draw.line(((x_label_left, y), (width - 60, y)), fill="#ccc", width=1)
        y += 20

        # Test Centre with Background
        test_centre_bg_y1 = y
        draw.text((x_label_left, y), "Test Centre", font=font_section, fill="black")
        y += 40 # Increased spacing
        draw.text((x_label_left + 20, y), "Mominabad General Hospital", font=font_bold, fill="black")
        test_centre_bg_y2 = y + 35
        draw.rectangle((x_label_left - 10, test_centre_bg_y1 - 10, width - 50, test_centre_bg_y2 + 10), fill=("#e3f2fd"))
        draw.text((x_label_left, test_centre_bg_y1), "Test Centre", font=font_section, fill="black")
        draw.text((x_label_left + 20, y), "Mominabad General Hospital", font=font_bold, fill="black")
        y = test_centre_bg_y2 + 25

        # Section Divider
        draw.line(((x_label_left, y), (width - 60, y)), fill="#ccc", width=1)
        y += 20

        # Instructions (Left) and Signature (Right) Section
        draw.text((x_label_left, y), "Instructions", font=font_section, fill="black")
        y_notes_cursor = y + 45 # Increased spacing

        notes = [
            "Arrive 30 minutes before the test.",
            "Bring your Admit Card and original CNIC/B-Form.",
            "Mobile phones and gadgets are not allowed.",
            "No entry after the test starts."
        ]
        for note in notes:
            draw.text((x_label_left + 30, y_notes_cursor), note, font=font_note, fill="black")
            draw.text((x_label_left, y_notes_cursor), "•", font=font_note, fill=header_color)
            y_notes_cursor += 38 # Increased spacing for notes

        # Signature Box
        sig_x_start = width - 400 # Adjusted position
        sig_x_end = width - 80
        sig_y_top = y_notes_cursor - 60 # Adjusted position
        sig_y_bottom = y_notes_cursor
        draw.rectangle((sig_x_start - 10, sig_y_top - 5, sig_x_end + 10, sig_y_bottom + 5), fill="#f0f0f0")
        sig_y_line = y_notes_cursor - 25
        draw.line((sig_x_start, sig_y_line, sig_x_end, sig_y_line), fill="black", width=2)
        draw.text((sig_x_start, sig_y_line + 10), "Authorized Signature", font=font_signature, fill="black")

        # Display card and download button
        st.markdown("---")
        st.subheader("📎 Admit Card Preview")
        buf = io.BytesIO()
        card.save(buf, format="PNG")
        st.image(buf.getvalue(), use_container_width=True)

        st.download_button("⬇️ Download Admit Card", data=buf.getvalue(),
                          file_name=f"AdmitCard_{name.replace(' ', '_')}.png", mime="image/png")

        # Upload to Google Drive (Unchanged)
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