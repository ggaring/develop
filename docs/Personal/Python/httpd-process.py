#!/usr/bin/python
import subprocess
#from .logger import logger


class HttpdError():
	"""
	Httpd is not running, terminating deployment now!
	"""
	pass

class CheckApache(self):
	process = subprocess.Popen(["ps", "-e"], stdout=subprocess.PIPE)
	out, err = process.communicate()

	if ('httpd' in str(out)):
		print('Httpd running, proceeding on next steps...')
	else: 
		msg = 'Httpd is not started, stoping the deployment now!'
		raise HttpdError(msg)
		