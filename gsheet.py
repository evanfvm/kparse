
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime
import numpy as np
import pandas as pd
import streamlit as st

class gsheet ():
    def __init__(self, INFO, GMAIL="evan.fvm@gmail.com"):
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        self.permission = {
            'type': 'user',
            'role': 'reader',
            'emailAddress': GMAIL,
        }
        CREDS = Credentials.from_service_account_info (INFO, scopes=self.SCOPES)
        self.service = build("sheets", "v4", credentials=CREDS)
        self.drive_service = build('drive', 'v3', credentials=CREDS)
        self.fileID = "1tzs5uZlBeEFuMnxepXTqHm5W6YoSAC4L3pZLJGf7f1Y"

    def new_workbook (self):
        try:
            #create spreadsheet
            outfile = "Export_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            spreadsheet = {"properties": {"title": outfile}}
            spreadsheet = (
                    self.service.spreadsheets()
                    .create(body=spreadsheet, fields="spreadsheetId")
                    .execute()
                )
            self.fileID = spreadsheet.get('spreadsheetId')

            # share permission
            request = self.drive_service.permissions().create(
                    fileId=self.fileID,
                    body=self.permission,
                )
            response = request.execute()

            return self.fileID

        except HttpError as err:
          return err

    def del_workbook (self):
        try:
            self.drive_service.files().delete(fileId=self.fileID).execute()
        except HttpError as err:
          print (err)




    def export (self, BLOCKS):
        # write MO data
        TABNAMES = sorted(np.unique(BLOCKS[:,0]))
        WORKBOOKS = {tab: pd.DataFrame(list(BLOCKS[BLOCKS[:,0]==tab, 1])) for tab in TABNAMES}
        try:
            #write data
            data = [{"range": tab, "values": pd.DataFrame(list(BLOCKS[BLOCKS[:,0]==tab, 1])).to_numpy().tolist()} for tab in TABNAMES]
            body = {"valueInputOption": "USER_ENTERED", "data": data}
            response = (
                self.service.spreadsheets()
                .values()
                .batchUpdate(spreadsheetId=self.fileID, body=body)
                .execute()
            )

        except HttpError as err:
            print (err)


        # writer = pd.ExcelWriter(OUTFILE, engine="openpyxl")
        # [WORKBOOKS[tab].to_excel(writer, sheet_name=tab[:31], index=False) for tab in TABNAMES]
        # writer.close()
if __name__ == "__main__":
    gc = gsheet(st.secrets['gsheets'])
    gc.del_workbook()
