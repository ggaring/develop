from __future__ import absolute_import
import os
import json
import sys
from logger import logger

PROJECT_FILE = 'shipit.json'
PROJECT_DIR = os.path.abspath(os.getcwd())
#CONFIG = os.path.join(PROJECT_DIR, PROJECT_FILE)

print(PROJECT_FILE)
print(PROJECT_DIR)
#print(CONFIG)

class Configuration(object):
	def __init__(self, configuration):
		self.project_path = os.path.dirname(configuration)
		try:
			with open(configuration) as json_conf:
				self.json = json.loads(json_conf.read())
		except IOError:
				msg = "Cannot find configuration file: {}".format(configuration)
				logger.fatal(msg)
				sys.exit(1)

def main():
	if CONFIG:
		Configuration(CONFIG)
	else: 
		msg = "{} is not existing".format(Configuration)
		logger.debug(msg)
		sys.exit(1)

if __name__ == '__main__':
	main()