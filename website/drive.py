# 📦 Standard Libraries
import os

# 🌐 Third-Party Libraries
from dotenv import load_dotenv
from google.auth import default
from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload

# 🔐 Load environment variables from .env
load_dotenv()

# 📁 Config from environment
FOLDER_ID = os.getenv(
    "WEBSITE_DRIVE_FOLDER_ID"
)  # Target Google Drive folder for upload
GOOGLE_SA_FILE = os.getenv("GOOGLE_SA_FILE")  # Path to service account credentials
SCOPES = ["https://www.googleapis.com/auth/drive.file"]  # Required Google Drive scope


# 🔐 Authenticate using service account and return a Drive API client
def authenticate_google_drive():
    if not GOOGLE_SA_FILE:
        raise ValueError("⚠️ GOOGLE_SA_FILE not set in .env")

    creds, _ = default(scopes=SCOPES)

    return build("drive", "v3", credentials=creds)


# 📤 Upload a DOCX file from memory to Google Drive (as a Google Doc)
def upload_docx_to_gdrive(docx_stream, filename):
    service = authenticate_google_drive()

    file_metadata = {
        "name": filename,
        "parents": [FOLDER_ID],
        "mimeType": "application/vnd.google-apps.document",
    }

    docx_stream.seek(0)
    docx_content = docx_stream.read()

    media = MediaInMemoryUpload(
        docx_content,
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        resumable=True,
    )

    uploaded = (
        service.files()
        .create(
            body=file_metadata,
            media_body=media,
            fields="id, name",
            supportsAllDrives=True,
        )
        .execute()
    )

    print(f"✅ Uploaded to Google Drive as: {uploaded['name']} (ID: {uploaded['id']})")
    return uploaded["id"]
