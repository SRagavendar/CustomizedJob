from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import openpyxl

data = []

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://www.linkedin.com")
sign_in = driver.find_element_by_class_name('nav__button-secondary')
sign_in.click()
time.sleep(2)

username = driver.find_element_by_name('session_key')
username.send_keys('ragajks@gmail.com')

password = driver.find_element_by_name('session_password')
password.send_keys('Dudpotato@1096')
password.send_keys(Keys.RETURN)
time.sleep(5)

search = driver.find_element_by_xpath('//input[@class="search-global-typeahead__input always-show-placeholder"]')
search.send_keys('Enter jobs you want'+Keys.RETURN)
time.sleep(5)

toggle = driver.find_element_by_xpath('/html/body/div[8]/div/div/div/div/button').click()
time.sleep(3)

easyjob = driver.find_element_by_xpath('//span[text()="LinkedIn Features"]').click()
time.sleep(2)

check = driver.find_element_by_xpath('//span[text()="Easy Apply"]').click()
time.sleep(1)

apply = driver.find_element_by_xpath('/html/body/div[9]/div[4]/div/div[1]/header/div/div/div[2]/div/div/div/ul/li[1]/form/div/fieldset/div/div/div/button[2]').click()
time.sleep(7)

time = driver.find_elements_by_xpath('//li[starts-with(@id,"ember")]/div/div[2]/ul/li[1]/time')
time = [l.get_attribute("datetime") for l in time]
data.extend(time)

jobtitle = driver.find_elements_by_xpath('//li[starts-with(@id,"ember")]/div/div/div/h3/a')
jobtitle = [l.text for l in jobtitle]
data.extend(jobtitle)

companyname = driver.find_elements_by_xpath('//li[starts-with(@id,"ember")]/div/div/div/div/a')
companyname = [l.text for l in companyname]
data.extend(companyname)

location = driver.find_elements_by_xpath('//li[starts-with(@id,"ember")]/div/div/div/span')
location = [l.text for l in location]
data.extend(location)

joblink = driver.find_elements_by_xpath('//li[starts-with(@id,"ember")]/div/div/div/h3/a')
joblink = [l.get_attribute('href') for l in joblink]
data.extend(joblink)

skillmatch = driver.find_elements_by_xpath('//li[starts-with(@id,"ember")]/div/div[2]/div/div/div/div')
skillmatch = [l.text for l in skillmatch]

df = pd.DataFrame()

df['Date'] = time
df['Job Title'] = jobtitle
df['Company Name'] = companyname
df['Location'] = location
df['Job Apply Link'] = joblink

filename = 'LinkedInJobs.xlsx'
df.to_excel(filename, sheet_name='new_sheet', index = False)

'''
with pd.ExcelWriter(filename, engine='openpyxl') as writer:
    writer.book = openpyxl.load_workbook(filename)
    df.to_excel(writer, sheet_name='new_sheet', index=False)
    writer.save()
    '''