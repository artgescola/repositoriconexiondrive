from fastapi import FastAPI
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import json

app = FastAPI()

SERVICE_ACCOUNT_INFO = json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT"])

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

credentials = service_account.Credentials.from_service_account_info(
    SERVICE_ACCOUNT_INFO, scopes=SCOPES
)

sheets_service = build("sheets", "v4", credentials=credentials)

SPREADSHEET_ID = "1Qnn89Oz8KR8yPc6I8lkwi_uOZTqomLJv"


@app.get("/")
def root():
    return {"status": "alive"}


@app.post("/create-content")
def create_content(data: dict):
    try:
        row = data["excel_row"]

        values = [list(row.values())]

        sheets_service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range="A1",
            valueInputOption="RAW",
            body={"values": values}
        ).execute()

        return {"status": "ok"}

    except Exception as e:
        return {"error": str(e)}
