import os, logging, sqlite3, configparser
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from scripts.web import sign_in_to_indeed, search_preference, fetch_all_jobs_from_page,\
    parse_apply_w_indeed_resume, apply, next_web_page, construct_container
from scripts.database import *
from scripts.logger import *

config_app = configparser.ConfigParser()
config_app.read('app.ini')
py_indeed_configs = config_app['py_indeed']

chrome_option = Options()
chrome_option.add_argument("--headless")
chrome_option.add_argument("--window-size=1366,768")
chrome = webdriver.Chrome(executable_path=(os.getcwd() + r'\chromedriver.exe'),
                          options=chrome_option)
connection_to_db = sqlite3.connect("questions__answers_db.db")
cursor = connection_to_db.cursor()
data_table_creation(cursor, connection_to_db)
general_runtime_logger = create_general_logger(__name__, level="INFO")
data_container = construct_container()
email_address = py_indeed_configs['email_address']
password = py_indeed_configs['password']
job_title = py_indeed_configs['job_title']
location = py_indeed_configs['location']

def main():
    signed_in = sign_in_to_indeed(chrome, email_address, password)
    if(signed_in):
        search_preference(chrome, job_title, location)
        while(True):
            jobs = fetch_all_jobs_from_page(chrome)
            jobs_indeed_resume = parse_apply_w_indeed_resume(jobs)
            apply(chrome, jobs_indeed_resume, cursor, connection_to_db, data_container)
            next_web_page(chrome)
    else:
        general_runtime_logger.error("Could not sign into indeed account...")

def test_main():
    sign_in_to_indeed(chrome, email_address, password)
    jobs_indeed_resume = []
    apply(chrome, jobs_indeed_resume, cursor, connection_to_db, data_container)

main()
#test_main()

connection_to_db.close()
logging.shutdown()