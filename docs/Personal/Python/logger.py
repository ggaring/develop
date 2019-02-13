import os
import logging

# Assume logging is set into INFO
formatter = ' %(message)s'
level = logging.INFO

if os.environ.get('DEBUG_MODE') == "1":
	# unless DEBUG_MODE is set to 1
	# configuring logging
	formatter = '%(asctime)s - %(levelname)-9s - %(message)s'
	level = logging.DEBUG

# set the logger
logging.basicConfig(level=level, format=formatter)
logger = logging.getLogger(__name__)