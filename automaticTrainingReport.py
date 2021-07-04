from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

#google sheets code
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('iconic-heading-318603-c8baf39d791a.json', scope)
client = gspread.authorize(creds)
sheet = client.open('Test')
sheet_instance = sheet.get_worksheet(0)


PATH = "/Users/moogle/Desktop/chromedriver" #locates path of chromedriver and saves it to PATH

chrome_options = Options()
#chrome_options.add_argument("--headless")

driver = webdriver.Chrome(PATH,options = chrome_options) #sets the webdriver to variable driver (which is basically like opening up the chrome browser)

#logs into qualio using any username and password
def login (username, password):
    driver.find_element_by_id('input-email').send_keys(username)
    driver.find_element_by_id('input-password').send_keys(password)
    driver.find_element_by_id('login-btn').click()

driver.get("https://app.qualio.com/login")
login('xxx','xxx')
time.sleep(5)

#finds the training button and clicks on it
driver.find_element_by_xpath('//*[@id="header"]/navigation-menu-container/nav/div/div[2]/ul[1]/li[3]').click()

#finds the training overview button and clicks on it
driver.find_element_by_xpath('//*[@id="header"]/navigation-menu-container/nav/div/div[2]/ul[1]/li[3]/ul/li/a').click()

#time for the next page to load
time.sleep(5)


allTimeBtn = driver.find_element_by_xpath('//*[@id="ng-app"]/body/span/div/div/div[2]/div/div[1]/div[1]/whitebox/div/div/div/div/div[2]/select')
for option in allTimeBtn.find_elements_by_tag_name('option'):
    if option.text == 'Last 30 days':
        option.click()
        break

time.sleep(5)

completedText = int(driver.find_element_by_xpath('//*[@id="ng-app"]/body/span/div/div/div[2]/div/div[1]/div[1]/whitebox/div/div/div/div/div[2]/div[2]/completed-training-metric-card/metric-card/div/div[1]').text)
overdueText = int(driver.find_element_by_xpath('//*[@id="ng-app"]/body/span/div/div/div[2]/div/div[1]/div[1]/whitebox/div/div/div/div/div[2]/div[2]/overdue-training-metric-card/metric-card/div/div[1]').text)
compliantPercentage = (completedText - overdueText) / completedText * 100
print('Compliant Percentage: ' + str(((completedText - overdueText) / completedText) * 100) + '%')

time.sleep(5)

sheet_instance.update_cell(1,1, "Completed: ")
sheet_instance.update_cell(1,2, completedText)
sheet_instance.update_cell(2,1, "Overdue: ")
sheet_instance.update_cell(2,2, overdueText)
sheet_instance.update_cell(3,1, "Compliant %: ")
sheet_instance.update_cell(3,2, "=TO_PERCENT((B1-B2)/B1)")

driver.quit()