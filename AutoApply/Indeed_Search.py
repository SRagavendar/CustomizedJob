import os, logging, sqlite3, configparser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

config_app = configparser.ConfigParser()
config_app.read('app.ini')
Indeed_Search_configs = config_app['Indeed_Search']

chrome_option = Options()
chrome_option.add_argument("--headless")
chrome_option.add_argument("--window-size=1366,768")
chrome = webdriver.Chrome(executable_path=(os.getcwd() + '\chromedriver.exe'), options=chrome_option)

connection_to_db = sqlite3.connect("stuff.db")
cursor = connection_to_db.cursor()
data_table_creation(cursor, connection_to_db)

general_runtime_logger = create_general_logger(__name__, level="INFO")

data_tupperware = construct_tupperware()
email_address = Indeed_Search_configs['email_address']
password = Indeed_Search_configs['password']
job_title = Indeed_Search_configs['job']
location = Indeed_Search_configs['location']

def main():
    signedIn = sign_in_Indeed(chrome, email_address, password)
    if (signedIn):
        search_preference(chrome, job_title, location)
        while(True):
            jobs = fetch_all_jobs(chrome)
            jobs_resume = parse_apply_indeed_resume(jobs)
            apply(chrome, jobs_resume, cursor, connection_to_db, data_tupperware)
            next_web_page(chrome)
    else:
        general_runtime_logger.error("COuld not sign into Indeed account")

def test():
    sign_in_Indeed(chrome, email_address, password)
    jobs_resume = []
    apply(chrome, jobs_resume, cursor, connection_to_db, data_tupperware)

#main()
test()

connection_to_db.close()
logging.shutdown()
