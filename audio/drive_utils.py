# 📦 Standard Libraries
import os
import io
import tempfile

# 🌐 Third-Party Libraries
from dotenv import load_dotenv
from google.auth import default
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload

# 🔐 Load environment variables
load_dotenv()

# 🔧 Config: Path to service account + Drive API scopes
GOOGLE_SA_FILE = os.getenv("GOOGLE_SA_FILE")
SCOPES = ["https://www.googleapis.com/auth/drive"]


# 📡 Authenticate using a service account and return a Drive API client
def get_drive_service():
    creds, _ = default(scopes=SCOPES)  # ✅ Uses Cloud Run attached service account
    return build("drive", "v3", credentials=creds)


# ⬇️ Download a file (e.g., audio) from Google Drive and save it temporarily
def download_audio_from_drive(file_id):
    service = get_drive_service()
    request = service.files().get_media(fileId=file_id)

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".m4a")
    downloader = MediaIoBaseDownload(temp_file, request)
    done = False

    while not done:
        status, done = downloader.next_chunk()
        print(f"Downloading audio: {int(status.progress() * 100)}%")

    temp_file.close()
    return temp_file.name


# 📤 Upload a DOCX file to Google Drive (from memory)
def upload_file_to_drive_in_memory(file_data, folder_id, final_name="Summary.docx"):
    service = get_drive_service()

    file_metadata = {"name": final_name, "parents": [folder_id]}
    file_stream = io.BytesIO(file_data)

    media = MediaIoBaseUpload(
        file_stream,
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        resumable=True,
    )

    file = (
        service.files()
        .create(
            body=file_metadata,
            media_body=media,
            fields="id",
            supportsAllDrives=True,
        )
        .execute()
    )

    print(f"📤 File uploaded: {file.get('id')}")
    return file.get("id")


# 🔍 Find the first audio file in a folder by extension
def find_audio_file_in_folder(folder_id, extension=".m4a"):
    service = get_drive_service()
    query = f"'{folder_id}' in parents"
    results = (
        service.files()
        .list(
            q=f"'{folder_id}' in parents",
            fields="files(id, name)",
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
        )
        .execute()
    )

    files = results.get("files", [])

    for file in files:
        if file["name"].lower().endswith(extension):
            print(f"🎯 Found audio file: {file['name']}")
            return file["id"]

    print("⚠️ No .m4a file found in folder.")
    return None


# 🔍 Try to find a folder matching keywords from the company name
def find_folder_id_by_partial_name(company_name, parent_folder_id):
    service = get_drive_service()

    # 🔍 Get all folders under the parent folder
    query = f"mimeType='application/vnd.google-apps.folder' and '{parent_folder_id}' in parents"
    response = (
        service.files()
        .list(
            q=query,
            fields="files(id, name)",
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
        )
        .execute()
    )

    folders = response.get("files", [])
    company_keywords = company_name.lower().split()

    # ✅ Partial keyword match: any keyword in folder name
    for folder in folders:
        folder_name = folder["name"].lower()
        if any(keyword in folder_name for keyword in company_keywords):
            print(f"📁 Matched folder: {folder['name']}")
            return folder["id"]

    print(f"❌ No folder matched any part of: {company_name}")
    return None
