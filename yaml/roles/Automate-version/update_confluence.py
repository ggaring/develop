#!/usr/bin/env python
"""
Automated way of displaying the latest version per product
"""

import json
import requests
import argparse
import datetime
import logging
from json2html import *
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# setting the confluence-page api url
BASE_URL = 'https://confluence-poc.ph.esl-asia.com/rest/api/content/21627224'
#PAGE_ID = '21627224'

# setting the logger
LOG_FILE = "confluence.log"
formatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(formatter)
logger = logging.getLogger('confluence automation')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# setting the date
now = datetime.datetime.now()

def extract_info():
	url = '{}'.format(BASE_URL)

	info = requests.get(url, auth=('ggaring', 'Emcee_06'), verify=False)
	info.raise_for_status()

	return (info.json())

def update_jsonfile(product, version):
	"""
	This is where the magic will happen
	"""
	jsonfile = open("info.json", "r")
	data = json.load(jsonfile)
	jsonfile.close()

	# This part will open the json file and store the current data to tmp
	# Then this is where the new version will be assigned to that existing json key
	tmp = data['products'][product]['latest version']
	data['products'][product]['latest version'] = version


	jsonfile = open("info.json", "w+")
	# after changing the value of the variable, this will overwrite
	# the current json file
	jsonfile.write(json.dumps(data))
	jsonfile.close()


	jsonfile = open("info.json", "r")
	data = json.load(jsonfile)
	input = data

	# conversion of json format to html table format
	htmlOutput = json2html.convert(json = input)

	return htmlOutput

def update_content(html):
	# get the needed values
	auth=('ggaring', 'Emcee_06')
	info = extract_info()
	page_id = info['id']
	title = info['title']
	version = info['version']['number']
	ver = int(version) + 1

	conf_content = "<h2>Updated last: <i>" +str(now.strftime("%Y-%m-%d %H:%M") +"</i></h2>")
	# this will append the actual html table
	conf_content += html

	data = {
		"id" : str(page_id),
        "type" : "page",
        "title" : title,
        "version" : {"number": ver},
        "body"  : {
        	'storage' :
            {
            	"value" : str(conf_content),
                "representation" : "storage",
            }
        }
    }

    # this will dump the new content to data
	data = json.dumps(data)
	url = '{}?expand=body.storage'.format(BASE_URL)

	# then this will the new json content to confluence page via PUT method
	r = requests.put(
		url,
		data = data,
		auth = auth,
		headers = { 'Content-Type' : 'application/json' },
		verify = False
		)

	r.raise_for_status()

	# this will display if triggered via cli
	print('Wrote {} version {}'.format(title, ver))

def main():
	"""
	This is the main function, this is where all the stuff will happen
	It will prompt you to enter two(2) parameter: product and version
	"""
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"product",
		type = str,
		default = None,
		help = 'Please specify what product will be updated'
		)

	parser.add_argument(
		"version",
		type = str,
		default = None,
		help = 'Please specify the product version'
		)

	options = parser.parse_args()

	# this will open the json file for reference
	jsonfile = open("info.json", "r")
	data = json.load(jsonfile)

	logger.info('Checking if {} is included on the valid products'.format(options.product))
	if options.product in data['products']:
		logger.info('{} is a valid product'.format(options.product))
		# then this will check if the product passed on paramater is on the json file
		htmlcontent = update_jsonfile(options.product, options.version)
		update_content(htmlcontent)
		logger.info('Confluence page now updated!')
	else:
		# will throw an error is you passed an invalid product name
		logger.error('{} is an invalid project name'.format(options.product))
		raise Exception('Product name passed on parameter is not valid!')

if __name__ == '__main__':
	logger.info('Running the script now')
	main()