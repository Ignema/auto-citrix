import gspread
from time import sleep
import json

# Load config
config = json.load(open("config.json", "r"))

# Configure Google Spreadsheets Client
client = gspread.service_account("credentials.json")
s = client.open(config["sheet_name"]).sheet1

def get_latest_sms_code():
    code = find_new_sms()
    while code == 0:
        sleep(1)
        code = find_new_sms()
    return code

def find_new_sms():
    sheet = fetch_sheet()
    for i in range(len(sheet)):
        if sheet[i][3] == "No":
            s.update_cell(i + 2, 4, "Yes")
            return sheet[i][2]
    return 0

def fetch_sheet():
    return s.get_all_values()[1:]