# 📦 Standard Libraries
import os

# 🌐 Third-Party Libraries
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

# 🔐 Load environment variables from .env
load_dotenv()

# Google Sheet ID and service account key path from .env
SHEET_ID = os.getenv("GOOGLE_SHEET_ID")        # Unique identifier of the Google Sheet
CREDENTIALS_PATH = os.getenv("GOOGLE_SA_FILE") # Path to the service account credentials JSON


# 📥 Get all rows that are pending processing
def get_pending_rows():

    # Define the required Google API scopes
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    
    # 🔐 Authenticate using the service account
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_PATH, scope)
    client = gspread.authorize(creds)
    
    # Open the first worksheet in the specified sheet
    sheet = client.open_by_key(SHEET_ID).sheet1
    records = sheet.get_all_values()

    # 🟡 Filter for rows that have both website and audio links and are not marked "done"
    pending = []
    for idx, row in enumerate(records[1:], start=2):    # Skip header (row 0)
        website = row[4].strip() if len(row) >= 5 else ""
        audio = row[5].strip() if len(row) >= 6 else ""
        status = row[8].strip().lower() if len(row) >= 9 else ""

        # ✅ Add row index and relevant data if ready to process
        if website and audio and status != "done":
            pending.append((idx, website, audio))

    return pending


# 📤 Update a row in the Google Sheet with summary links and status
def update_sheet_with_links( row_index, meeting_url=None, meeting_name=None, website_url=None, website_name=None):
    
    # Define the required scopes
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    # 🔐 Authenticate again for sheet update
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_PATH, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SHEET_ID).sheet1
    wrote_something = False
    
    # ✏️ Insert meeting (audio) summary hyperlink into column 7 (G)
    if meeting_url and meeting_name:
        formula = f'=HYPERLINK("{meeting_url}", "{meeting_name}")'
        sheet.update_cell(row_index, 7, formula)
        wrote_something = True
    
    # ✏️ Insert website summary hyperlink into column 8 (H)
    if website_url and website_name:
        formula = f'=HYPERLINK("{website_url}", "{website_name}")'
        sheet.update_cell(row_index, 8, formula)
        wrote_something = True
    
    # ✅ Mark the row as done if any link was updated
    if wrote_something:
        sheet.update_cell(row_index, 9, "Done")