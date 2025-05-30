import gspread
from google.oauth2.service_account import Credentials

# Set your spreadsheet name and credentials file path
SPREADSHEET_NAME = "UK Probate Divorce CRM"  # <-- Replace with your actual sheet name
SERVICE_ACCOUNT_FILE = "backend/credentials/service_account.json"  # <-- Update path if needed

def add_user_to_google_sheet(email, name):
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
    gc = gspread.authorize(creds)
    sh = gc.open(SPREADSHEET_NAME)
    worksheet = sh.sheet1  # or sh.worksheet("Sheet1")
    worksheet.append_row([email, name])
