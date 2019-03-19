import logging

LOG_FILE = 'app.log'

formatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(formatter)
logger = logging.getLogger('cms deployment cleanup')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def display_content():
	logger.info('this is the first debug file')

if __name__ == '__main__':
	logger.info('running the test logging file')
	display_content()