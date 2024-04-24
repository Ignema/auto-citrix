from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import chromedriver_autoinstaller
from sms import get_latest_sms_code, reset_sms
from time import sleep
import json

from sms import get_latest_sms_code

# Load config
config = json.load(open("config.json", "r"))

# Install chrome driver if it's missing
chromedriver_autoinstaller.install()

# Suppressing logs in console
options = Options()
options.add_argument('--log-level=3')

# Reset SMS sheet
reset_sms()


# Start browser and navigate to page
browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
browser.get(config["citrix_url"])

# Insert cookie to avoid alert message later
browser.add_cookie({"name":"CtxsClientDetectionDone", "value":"true"})


# Login Page
WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.ID, "login")))
browser.find_element(By.ID, "login").send_keys(config["user"])
browser.find_element(By.ID, "passwd").send_keys(config["password"])
browser.find_element(By.ID, "nsg-x1-logon-button").click()


# 2FA Page
if(config["auto_sms"]):
    code = get_latest_sms_code()
else:
    code = input("Please enter the 2FA you received on your phone: ")
WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.ID, "response")))
browser.find_element(By.ID, "response").send_keys(code)
browser.find_element(By.ID, "ns-dialogue-submit").click()


# Citrix Dashboard
WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.ID, "desktopsBtn")))
browser.find_element(By.ID, "desktopsBtn").click()
WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "storeapp-details-link")))
browser.find_element(By.CLASS_NAME, "storeapp-details-link").click()

# Delay to download .ica file and let user open it
sleep(15)