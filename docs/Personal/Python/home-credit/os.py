import os
from datetime import datetime

#print(os.getcwd())

#mod_time = os.stat('demo.txt').st_mtime
#print(datetime.fromtimestamp(mod_time))
os.chdir('/home/ggaring/Desktop')

#for dirpath, dirnames, filenames in os.walk(os.getcwd()):
#	print('Current Path:', dirpath)
#	print('Directories:', dirnames)
#	print('Files:', filenames)
#	print()

print(os.environ.get('HOME'))