# 📦 Standard Libraries
import os

# 🌐 Third-Party Libraries
import gspread
from google.auth import default
from dotenv import load_dotenv

# 🔐 Load environment variables from .env
load_dotenv()

# Google Sheet ID from .env
SHEET_ID = os.getenv("GOOGLE_SHEET_ID")  # Unique identifier of the Google Sheet

# Common Google API scopes
SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


# 📥 Get all rows that are pending processing
def get_pending_rows():
    """
    Fetch rows from the Google Sheet that have website and audio links but are not marked 'done'.
    Returns a list of tuples (row_index, website_link, audio_link).
    """
    # 🔐 Authenticate using Cloud Run's attached service account
    creds, _ = default(scopes=SCOPES)
    client = gspread.authorize(creds)

    # Open the first worksheet in the specified sheet
    sheet = client.open_by_key(SHEET_ID).sheet1
    records = sheet.get_all_values()

    # 🟡 Filter for rows that have both website and audio links and are not marked "done"
    pending = []
    for idx, row in enumerate(records[1:], start=2):  # Skip header (row 0)
        website = row[4].strip() if len(row) >= 5 else ""
        audio = row[5].strip() if len(row) >= 6 else ""
        status = row[8].strip().lower() if len(row) >= 9 else ""

        # ✅ Add row index and relevant data if ready to process
        if website and audio and status != "done":
            pending.append((idx, website, audio))

    return pending


# 📤 Update a row in the Google Sheet with summary links and status
def update_sheet_with_links(
    row_index, meeting_url=None, meeting_name=None, website_url=None, website_name=None
):
    """
    Update a row in the Google Sheet with meeting and/or website links, and mark it as done.
    """
    # 🔐 Authenticate using Cloud Run's attached service account
    creds, _ = default(scopes=SCOPES)
    client = gspread.authorize(creds)

    sheet = client.open_by_key(SHEET_ID).sheet1
    wrote_something = False

    if meeting_url and meeting_name:
        formula = f'=HYPERLINK("{meeting_url}", "{meeting_name}")'
        sheet.update_cell(row_index, 7, formula)
        wrote_something = True

    if website_url and website_name:
        formula = f'=HYPERLINK("{website_url}", "{website_name}")'
        sheet.update_cell(row_index, 8, formula)
        wrote_something = True

    if wrote_something:
        sheet.update_cell(row_index, 9, "Done")
