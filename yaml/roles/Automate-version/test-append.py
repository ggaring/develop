import json
import requests
import argparse
import datetime

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = 'https://confluence-poc.ph.esl-asia.com/rest/api/content/'
#BASE_URL = 'https://confluence.ph.esl-asia.com/rest/api/content/'
PAGE_ID = '21627224'
VIEW_URL = "http://confluence-poc.ph.esl-asia.com/pages/viewpage.action?pageId=21627224"

now = datetime.datetime.now()# Version = []
# Default_Product = ['Account', 'Sportsbook']


# New_entry = 'Entrypage'

# if New_entry in Product:
# 	print(New_entry+" is already on products list")
# else:
# 	print(New_entry+" is not existing, appending it now on products list")
# 	Product.append(New_entry)

# print(Product)

def get_page_version(page_id):
	url = '{base}/{page_id}'.format(
		base = BASE_URL,
		page_id = page_id)

	info = requests.get(url, auth=('ggaring', 'Emcee_06'), verify=False)
	info.raise_for_status()

	return (info.json()['version']['number'])

def get_page_title(page_id):
	url = '{base}/{page_id}'.format(
		base = BASE_URL,
		page_id = page_id)

	info = requests.get(url, auth=('ggaring', 'Emcee_06'), verify=False)
	info.raise_for_status()

	return (info.json()['title'])

def get_page_content(page_id):
	url = '{base}/{page_id}?expand=body.storage'.format(
		base = BASE_URL,
		page_id = page_id)

	cont = requests.get(url, auth=('ggaring', 'Emcee_06'), verify=False)
	cont.raise_for_status()

	return (cont.json()['body']['storage']['value'])

if __name__ == '__main__':
	print(get_page_content(PAGE_ID))
