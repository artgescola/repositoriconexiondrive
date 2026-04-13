from fastapi import FastAPI
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import json

app = FastAPI()

# 🔐 Leer credenciales desde variable de entorno
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
docs_service = build("docs", "v1", credentials=credentials)

# 🔧 CONFIGURA ESTO
SPREADSHEET_ID = "1rXOWiOc3RbOejxs4oHQZJc3cWQxzhbMs"
FOLDER_ID = "1xRTWRA2WrQcrzbfR3miCT4GghA-DVWzn"


@app.post("/create-content")
def create_content(data: dict):

    nombre = data["nombre_doc"]
    contenido = data["contenido_doc"]
    row = data["excel_row"]

    # 📄 Crear documento en Drive (FORZANDO uso de tu Drive)
    file_metadata = {
        "name": nombre,
        "mimeType": "text/plain",
        "parents": [FOLDER_ID]
    }

    file = drive_service.files().create(
        body=file_metadata,
        fields="id",
        supportsAllDrives=True
    ).execute()

    doc_id = file.get("id")

    # ✍️ Escribir contenido
    docs_service.documents().batchUpdate(
        documentId=doc_id,
        body={
            "requests": [
                {
                    "insertText": {
                        "location": {"index": 1},
                        "text": contenido
                    }
                }
            ]
        }
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
