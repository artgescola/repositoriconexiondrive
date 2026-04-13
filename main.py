from fastapi import FastAPI
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import json
from io import BytesIO
from googleapiclient.http import MediaIoBaseUpload

app = FastAPI()

# 🔐 Credenciales
SERVICE_ACCOUNT_INFO = json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT"])

SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets"
]

credentials = service_account.Credentials.from_service_account_info(
    SERVICE_ACCOUNT_INFO, scopes=SCOPES
)

drive_service = build("drive", "v3", credentials=credentials)
sheets_service = build("sheets", "v4", credentials=credentials)

# 🔧 CONFIGURA ESTO
SPREADSHEET_ID = "1Qnn89Oz8KR8yPc6I8lkwi_uOZTqomLJv"
FOLDER_ID = "1xRTWRA2WrQcrzbfR3miCT4GghA-DVWzn"


@app.post("/create-content")
def create_content(data: dict):

    nombre = data["nombre_doc"]
    contenido = data["contenido_doc"]
    row = data["excel_row"]

    # 📄 Crear archivo TXT en Drive (SOLUCIÓN AL PROBLEMA DE QUOTA)
    file_metadata = {
        "name": f"{nombre}.txt",
        "parents": [FOLDER_ID]
    }

    media = MediaIoBaseUpload(
        BytesIO(contenido.encode("utf-8")),
        mimetype="text/plain"
    )

    file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id"
    ).execute()

    # 📊 Añadir fila al Excel
    values = [list(row.values())]

    sheets_service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range="A1",
        valueInputOption="RAW",
        body={"values": values}
    ).execute()

    return {"status": "ok"}
