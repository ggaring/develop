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

now = datetime.datetime.now()
#Defaults

#old_page_url: ''https://confluence-poc.ph.esl-asia.com/rest/api/content/'21627195'
#new_page_url: 'https://confluence-poc.ph.esl-asia.com/rest/api/content/17137829'

# def get_page_json(page_id, expand = False):
# 	if expand:
# 		suffix = "?exand=" + expand
# 		#body.storage
# 	else:
# 		suffix = ""

# 	url="https://confluence-poc.ph.esl-asia.com/rest/api/content/" + page_id + suffix
# 	response = requests.get(url, auth=('ggaring', 'Emcee_06'), verify=False)
# 	response.encoding = "utf8"
# 	return(json.loads(response.text))
def get_page_anscestors(page_id):
	url = '{base}/{page_id}?expand=body.storage'.format(
		base = BASE_URL,
		page_id = page_id)

	ansc = requests.get(url, auth=('ggaring', 'Emcee_06'), verify=False)
	ansc.raise_for_status()

	return ansc.json()['anscestors']

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

def get_page_info(page_id):
	url = '{base}/{page_id}'.format(
		base = BASE_URL,
		page_id = page_id)

	info = requests.get(url, auth=('ggaring', 'Emcee_06'), verify=False)
	info.raise_for_status()

	return (info.json())

def get_page_content(page_id):
	url = '{base}/{page_id}?expand=body.storage'.format(
		base = BASE_URL,
		page_id = page_id)

	cont = requests.get(url, auth=('ggaring', 'Emcee_06'), verify=False)
	cont.raise_for_status()

	return (cont.json()['body']['storage']['value'])

def update_content(page_id, html):
	auth=('ggaring', 'Emcee_06')
	conf_content = get_page_content(PAGE_ID)
	title = get_page_title(PAGE_ID)
	version = get_page_version(PAGE_ID)
	ver = int(version) + 1

	conf_content += "Updated last " +str(now.strftime("%Y-%m-%d %H:%M"))
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

	data = json.dumps(data)
	url = '{base}/{page_id}?expand=body.storage'.format(
		base = BASE_URL,
		page_id = page_id)

	r = requests.put(
		url,
		data = data,
		auth = auth,
		headers = { 'Content-Type' : 'application/json' },
		verify = False
		)

	r.raise_for_status()

	print('Wrote {} version {}'.format(title, ver))
	print('URL:  {}'.format(VIEW_URL))

def updateJsonfile(jsonfile):
	jsonfile = open("info.json", "r")
	data = json.load(jsonfile)
	jsonfile.close()

	print(data['products'][test_product]['latest version'])

	tmp = data['products'][test_product]['latest version']
	data['products'][test_product]['latest version'] = version

	jsonfile = open("info.json", "w+")
	jsonfile.write(json.dumps(data))
	jsonfile.close()



#=======================================================================
#=======================================================================
#=======================================================================



def main():
	parser = argparse.ArgumentParser()

	parser.add_argument(
		"-f",
		"--file",
		default = None,
		type = str,
		help = "Write the contents of FILE to the confluence page"
		)

	parser.add_argument(
		"html",
		type = str,
		default = None,
		nargs = '?',
		help = 'Write the immediate html string to confluence page'
		)


	options = parser.parse_args()

	if options.html is not None and options.file is not None:
		raise RuntimeError(
			"Can't specify both a file and an immediate html to write to page")

	if options.html:
		html = options.html

	else:
		with open(options.file, 'r') as fd:
			html = fd.read()

	update_content(PAGE_ID, html)


def extract_info(PAGE_ID):
	info = get_page_info(PAGE_ID)
	ver = int(info['version']['number'])
	title = info['title']

	print(title)

if __name__ == '__main__':
	main()
	# print(get_page_content(PAGE_ID))