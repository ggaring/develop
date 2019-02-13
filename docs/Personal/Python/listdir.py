import os

def print_directory_contents(sPath):
	for path in os.listdir(sPath):
		sPath = os.path.join(sPath, path)
		if os.path.isdir(sPath):
			print_directory_contents(sPath)
		else:
			print(sPath)


print_directory_contents('/home/ggaring/Desktop/Personal/Python') 