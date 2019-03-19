from json2html import *
import json

test_product = "Account"
version = "release-Alpine-base-xx"

def updateJsonfile():
	jsonfile = open("info.json", "r")
	data = json.load(jsonfile)
	jsonfile.close()

	for cont in data['products']:
		print(cont)

def main():
	jsonfile = open("info.json", "r")
	data = json.load(jsonfile)
	jsonfile.close()

	if test_product in data['products']:
		print(test_product+ " is in the valid list")
	else:
		print(test_product+ " is not in the valid list")

main()

	# tmp = data['products'][test_product]['latest version']
	# data['products'][test_product]['latest version'] = version



# 	jsonfile = open("info.json", "w+")
# 	jsonfile.write(json.dumps(data))
# 	jsonfile.close()

# 	jsonfile = open("info.json", "r")
# 	data = json.load(jsonfile)
# 	input = data

# 	htmlOutput = json2html.convert(json = input)

# 	return htmlOutput

# html = updateJsonfile()

# print(html)

