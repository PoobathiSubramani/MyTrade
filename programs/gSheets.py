"""
this program reads data from google sheets
"""

#imports for g Sheets
from unittest import result
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import pandas as pd

def getSheetService(credsPath):
    #create sheet object
    try:
        creds = Credentials.from_service_account_file(credsPath)
        service = build('sheets', 'v4', credentials=creds)
        return service
    except HttpError as err:
        print("exception: ", err)

def readAllSymbols(sheetId, sheetRange, service):
    sheetObj = service.spreadsheets()
    result = sheetObj.values().get(spreadsheetId=sheetId, range=sheetRange).execute()
    values = result.get('values',[])
    df = pd.DataFrame(values[1:], columns=values[0])
    return df

def writeSheet(sheetId, service, inputData):
    writeRequest = [{
    "range":"mySymbols!A:C",
    "majorDimension":"ROWS",
    "values":inputData
    }]
    data = {'valueInputOption':"RAW", "data":writeRequest}
    results = service.spreadsheets().values().batchUpdate(spreadsheetId=sheetId, body=data).execute()
    return results

#sheetService = getSheetService(credsPath=credsPath)
#dfSymbols = readSheet(sheetId=symbolListSheetId, sheetRange=symbolListRange, service=sheetService)
#print(dfSymbols)
""" 
# FOR WRITING
inputData = [['symbol','date','action'],['TATACOMM','2022/07/18','BUY'],['WIPRO','2022/07/18','BUY']]


results = writeSheet(sheetId=mySymbolsSheetId, service=sheetService, inputData=inputData)
print(results)
 """


