from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time


PATH = "/Users/moogle/Desktop/chromedriver" #locates path of chromedriver and saves it to PATH
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--window-size=1920,1080')
driver = webdriver.Chrome(PATH,options = chrome_options) #sets the webdriver to variable driver (which is basically like opening up the chrome browser)
driver.implicitly_wait(10)

def login (username, password):
    driver.find_element_by_id('input-email').send_keys(username)
    driver.find_element_by_id('input-password').send_keys(password)
    driver.find_element_by_id('login-btn').click()

#open qualio and login
print('Logging In...')
driver.get("https://app.qualio.com/login")
login('miguel.vargas@proscia.com','gokhut-fofqIp-zarni5')
print('Logged in!')

#open the library
print('Opening the Library')
driver.find_element_by_class_name("nav-documents").click()
driver.find_element_by_xpath('//*[@id="header"]/navigation-menu-container/nav/div/div[2]/ul[1]/li[2]/ul/li[2]/a').click()

firstName = 'Elbert'
lastName = 'Basolis'
fullName = firstName + ' ' + lastName

#search for the training plan
driver.find_element_by_xpath('//*[@id="searchQuery"]').send_keys(fullName)
driver.find_element_by_xpath('//*[@id="searchQuery"]').send_keys(Keys.RETURN)
print("Searching for " + fullName +  "'s Training Plan")
time.sleep(2)
driver.find_element_by_xpath('//*[@id="contentView"]/div/table/tbody/tr[1]').click()
print('Found Training Plan')

#find the table
tableRows = driver.find_elements_by_css_selector("tr")
documentIDs = []

print('Recording required trainings as per Training Plan')
for columns in tableRows:
    tdCollection = columns.find_elements_by_css_selector("td")
    if 'X' in tdCollection[2].text:
        #print(tdCollection[0].text)
        documentIDs.append(tdCollection[0].text)

#move to training
print('Moving to Training page')
driver.find_element_by_xpath('//*[@id="header"]/navigation-menu-container/nav/div/div[2]/ul[1]/li[3]').click()
driver.find_element_by_xpath('//*[@id="header"]/navigation-menu-container/nav/div/div[2]/ul[1]/li[3]/ul/li/a').click()

#find employee
print('Searching for ' + fullName + "'s Training record...")
driver.find_element_by_xpath('/html/body/span/div/div/div[2]/div/div[3]/ul/li[3]/a').click()
time.sleep(1)
employeeName = ''
employeeNameBtn = None
forwardBtn = driver.find_element_by_xpath('//*[@id="ng-app"]/body/span/div/div/div[2]/div/div[3]/div/div[3]/training-users-list/rich-data-table-widget/div[3]/div/zd-table-pagination/div/span/div/button[2]')
employeeFound = False

while forwardBtn.is_enabled():
    employeeTable = driver.find_element_by_xpath("/html/body/span/div/div/div[2]/div/div[3]/div/div[3]/training-users-list/rich-data-table-widget/table/tbody")
    employeeTableRows = employeeTable.find_elements_by_css_selector("tr")
    for rows in employeeTableRows:
        employeeTableRowData = rows.find_elements_by_css_selector("td")
        employeeNameBtn = employeeTableRowData[0]
        #print(employeeNameBtn.text)
        if employeeNameBtn.text == fullName:
            employeeNameBtn.click()
            print(fullName + ' found')
            employeeFound = True
            break
    if employeeFound == True:
        break
    forwardBtn.click()
    time.sleep(1)

driver.find_element_by_xpath('/html/body/span/div/div/div[2]/div/whitebox/div/div/div/employee-training-dashboard-list/div/div[2]/div/div/div/div/div/div/table/thead/tr/th[1]').click()

trainingsDone = []

forwardBtn = driver.find_element_by_xpath('//*[@id="ng-app"]/body/span/div/div/div[2]/div/whitebox/div/div/div/employee-training-dashboard-list/div/div[3]/div/div/div/button[2]')

print('Recording assigned and completed trainings')
while True:
    trainingTable = driver.find_element_by_xpath('//*[@id="ng-app"]/body/span/div/div/div[2]/div/whitebox/div/div/div/employee-training-dashboard-list/div/div[2]/div/div/div/div/div/div/table/tbody[1]')
    trainingTableRows = trainingTable.find_elements_by_css_selector("tr")
    for rows in trainingTableRows:
        trainingTableRowData = rows.find_elements_by_css_selector("td")
        if "QSP" in trainingTableRowData[0].text or "QM" in trainingTableRowData[0].text or "QP" in trainingTableRowData[0].text:
            #print(trainingTableRowData[0].text + " YES")
            trainingsDone.append(trainingTableRowData[0].text)
    if forwardBtn.is_enabled():        
        forwardBtn.click()
    else:
        break
print('Comparing trainings required with trainings completed/assigned')
for i in trainingsDone:
    if i in documentIDs:
        documentIDs.remove(i)

print("NEEDS THESE TRAININGS:")
for i in documentIDs:
    print(i)