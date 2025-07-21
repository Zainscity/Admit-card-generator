# 🎓 Admit Card Generator (with Google Drive + Sheets Integration)

This Streamlit-based web application allows users to generate **visually styled admit cards** with user information, and automatically:

- ✅ Saves the generated card image to your **Google Drive**
- ✅ Stores metadata (name, phone, CNIC, etc.) as a **JSON file**
- ✅ Logs all generated card details in a **Google Sheet**
- ✅ Supports access from any device (PC or phone) via web interface

---

## 📌 Features

- Generate beautifully designed Admit Cards in PNG format.
- Responsive and clear font layout for printing.
- Saves both card images and structured JSON data to Drive.
- Logs user input data with timestamps in a connected Google Sheet.
- Works across devices (cross-platform, mobile-friendly).
- Fully automated backend using Google Apps Script.

---

## 🧰 Tech Stack

- **Frontend**: Python, Streamlit
- **Image Processing**: PIL (Pillow)
- **Backend Storage**: Google Apps Script (for Drive + Sheets integration)
- **Hosting**: Streamlit Cloud or any local machine
- **Cloud Storage**: Google Drive
- **Logging**: Google Sheets

---

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/admit-card-generator.git
cd admit-card-generator
2. Install Requirements
bash
Copy code
pip install -r requirements.txt
3. Set Up Google Apps Script (Drive + Sheets)
✅ Step-by-Step:
Go to https://script.google.com

Create a new script project.

Replace Code.gs with:

javascript
Copy code
function doPost(e) {
  try {
    var folder = DriveApp.getFolderById("YOUR_FOLDER_ID_HERE");

    var data = e.parameter;
    var image = data.image;
    var metadata = JSON.parse(data.metadata);

    var decoded = Utilities.base64Decode(image);
    var blob = Utilities.newBlob(decoded, MimeType.PNG, "AdmitCard_" + metadata.name + ".png");
    folder.createFile(blob);

    var metaBlob = Utilities.newBlob(JSON.stringify(metadata, null, 2), MimeType.JSON, "Meta_" + metadata.name + ".json");
    folder.createFile(metaBlob);

    var sheet = SpreadsheetApp.openById("YOUR_SHEET_ID_HERE").getSheetByName("Sheet1");
    sheet.appendRow([
      new Date(),
      metadata.name,
      metadata.father_name,
      metadata.admit_card_no,
      metadata.programme,
      metadata.cnic,
      metadata.phone
    ]);

    return ContentService.createTextOutput("✅ Card, metadata & log saved.");
  } catch (err) {
    return ContentService.createTextOutput("❌ Error: " + err.toString());
  }
}
Create a new folder in your Google Drive called Admit Cards and copy its Folder ID (from the URL).

Create a new Google Sheet with the following columns in Sheet1:

pgsql
Copy code
Timestamp | Name | Father Name | Admit Card No | Programme | CNIC | Phone
Open View > Show manifest file and update appsscript.json:

json
Copy code
{
  "timeZone": "Asia/Karachi",
  "dependencies": {},
  "exceptionLogging": "STACKDRIVER",
  "runtimeVersion": "V8",
  "webapp": {
    "executeAs": "USER_DEPLOYING",
    "access": "ANYONE_ANONYMOUS"
  },
  "oauthScopes": [
    "https://www.googleapis.com/auth/script.external_request",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
  ]
}
Save and Deploy as a Web App:

Access: Anyone, even anonymous

Copy the Web App URL (you’ll use this in your Python code).

🎨 Streamlit Frontend
Key Features
Inputs:

Name

Father’s Name

Programme

CNIC

Phone Number

Passport-sized photo upload

Card Preview rendered in real-time.

"Generate & Save" button sends:

Base64 PNG image

Metadata JSON

POST request to Google Apps Script

Sample Code Structure:
admit_card_app.py

fonts/ (your TTF font files)

Uses st.image(..., use_container_width=True) (not deprecated use_column_width)

Saves image locally and to Google Drive

🌐 Deployment
Deploy Locally
bash
Copy code
streamlit run admit_card_app.py
Deploy to Streamlit Cloud
Push project to GitHub

Go to https://share.streamlit.io

Connect your repo and deploy

Use your public Google Apps Script Web App URL in the backend call

📁 Files Saved in Drive
/Admit Cards/AdmitCard_John Doe.png

/Admit Cards/Meta_John Doe.json

Google Sheet Log Example:
Timestamp	Name	Father Name	Card No	Programme	CNIC	Phone
2025-07-20 16:34:22	John Doe	Mr. Doe	1001	BCS	42101-123...	0300-123456

💡 Future Enhancements
Add Email functionality to send cards directly

Admin dashboard to view logs and downloads

QR code integration for verification

Bulk card generation via CSV upload

🛡️ License
MIT License. Free to use and modify.

👨‍💻 Author
Made with ❤️ by Zainscity
LinkedIn: Zain Ul Abideen
