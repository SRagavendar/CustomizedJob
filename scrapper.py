import argparse
import requests
from bs4 import BeautifulSoup

 def get_google_page(name):
 	query = name.replace(' ', '+')
 	URL = f"https://google/com/search?q={query}+careers"
 	resp = requests.get(URL)
 	if '.' in name:
 		name = name.split('.')[0]

 	if resp.status_code == 200:
 		soup = BeautifulSoup(resp.content, "html.parser")

 		for a in soup.find_all('a', href=True):
 			if 'url' in a['href']:
 				url_list = a['href'][7:].split('/')
 				
if __name__ == '__main__':
	