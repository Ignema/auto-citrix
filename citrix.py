from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from time import sleep
import json

# Load config
config = json.load(open("config.json", "r"))

# Install chrome driver if it's missing
chromedriver_autoinstaller.install()

# Suppressing logs in console
options = Options()
options.add_argument('--log-level=3')


# Start browser and navigate to page
browser = webdriver.Chrome(options=options)
browser.get(config["citrix_url"])

# Insert cookie to avoid alert message later
browser.add_cookie({"name":"CtxsClientDetectionDone", "value":"true"})


# Login Page
sleep(3)
browser.find_element(By.ID, "login").send_keys(config["user"])
browser.find_element(By.ID, "passwd").send_keys(config["password"])
browser.find_element(By.ID, "nsg-x1-logon-button").click()


# 2FA Page
sleep(1)
code = input("Please enter the 2FA you received on your phone: ")
browser.find_element(By.ID, "response").send_keys(code)
browser.find_element(By.ID, "ns-dialogue-submit").click()


# Citrix Dashboard
sleep(10)
browser.find_element(By.ID, "desktopsBtn").click()
browser.find_element(By.CLASS_NAME, "storeapp-details-link").click()

# Delay to download .ica file and let user open it
sleep(15)