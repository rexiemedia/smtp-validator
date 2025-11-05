import gspread
from oauth2client.service_account import ServiceAccountCredentials

def append_to_google_sheet(row):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key('YOUR_SPREADSHEET_ID').sheet1
    sheet.append_row(row, value_input_option='USER_ENTERED')
