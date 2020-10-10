from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd
import openpyxl

data = []
c = 0
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://www.linkedin.com")
sign_in = driver.find_element_by_class_name('nav__button-secondary')
sign_in.click()
time.sleep(2)
username = driver.find_element_by_name('session_key')
username.send_keys('LinkedIn id')

password = driver.find_element_by_name('session_password')
password.send_keys('LinkedIn pasword')
password.send_keys(Keys.RETURN)
time.sleep(5)

file = 'LinkedInJobs.xlsx'

df = pd.read_excel(file, sheet_name='new_sheet', usecols="E")
joblinks = df.values.tolist()

for i in range(0,7):
    data.extend(joblinks[i])

for link in data:
    driver.get(link)
    apply = driver.find_element_by_xpath('//button[@class="jobs-apply-button artdeco-button artdeco-button--3 artdeco-button--primary ember-view"]').click()
    time.sleep(2)
    c = c + 1
    
    try:

        number = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]/div/form/div/div[1]/div[3]/div[2]/div/div/input').send_keys('your mobile number')

        try:

            nxt = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]/div/form/footer/div[2]/button').click()
            time.sleep(2)

            upload = driver.find_element_by_name('file').send_keys('C:/Users/... your resume file location path')
            time.sleep(2)

            nxt2 = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]/div/form/footer/div[2]/button[2]').click()
            time.sleep(2)

        except:

            try:
                upload = driver.find_element_by_name('file').send_keys('C:/Users/... your resume file location path')
                time.sleep(2)
            except:
                continue
    except:
        continue


print('\n{} jobs are applied...'.format(c))