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
