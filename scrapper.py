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
 				if name in url_list[2]:
 					return '/'.join(url_fixer(url_list))
 					break
def url_fixer(url_list):
	if len(url_list[-1]) > 8:
		url_list[-1] = url_list[-1].split('&')[0]
	return url_list

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("name", help="name of the company", type=str)
	args = parser.parse_args()
	url - get_google_page(args.name)
	print(url)