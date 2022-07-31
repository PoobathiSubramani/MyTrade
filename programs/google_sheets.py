import gspread
from google.oauth2.service_account import Credentials

scope = ['https://www.googleapis.com/auth/spreadsheets','https://googleapis.com/auth/drive']

credsJsonFile = '/Users/boopathi/Experiments/myTrade/keys/credentials.json'

creds = Credentials.from_service_account_file(credsJsonFile)
gClient = gspread.authorize(creds)
sheetSymbols = gClient.open_by_key('1XoVUOt6cV5iVj8Ma5nHjkCZoWZTiJYjQI8miv4k3R-I').symbolsList
print(sheetSymbols.get_all_records())