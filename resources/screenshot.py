#To execute this file, one needs to install selenium by: pip3 install selenium
#Furthermore, one needs to download chromedriver. See https://sites.google.com/a/chromium.org/chromedriver/downloads
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import sys
import os
import time
import csv
import simplejson as json
from PIL import Image
from urllib.parse import urlsplit, parse_qs
import urllib.request

def main(latitude, longitude):
	bg_url = 'https://revision.lewis.ucla.edu/arcgis/rest/services/ACS/ACS0610_NoTile/MapServer/0/query?geometry='+longitude+','+latitude+'&geometryType=esriGeometryPoint&inSR=4269&spatialRel=esriSpatialRelIntersects&outFields=GEOID&returnGeometry=false&returnIdsOnly=false&returnCountOnly=false&returnZ=false&returnM=false&returnDistinctValues=false&f=pjson'
	contents = urllib.request.urlopen(bg_url).read()
	json_response = json.loads(contents)
	print(json_response)
	geoid = json_response["features"][0]["attributes"]["GEOID"]
	#print(geoid)

	directory = "./save"
	if not os.path.exists(directory):
		os.makedirs(directory)
	row = []

	curr_time = time.time()
	options = webdriver.ChromeOptions()
	options.add_argument('--ignore-certificate-errors')
	options.add_argument("--test-type")
	options.binary_location = "/usr/bin/chromium"
	driver = webdriver.Chrome('/home/dja/Documents/projects/ITS/twitterBot/resources/chromedriver') #replace ... with a proper path to the chromedriver
	driver.maximize_window()

	driver.get('http://revision.lewis.ucla.edu/details/index.html?geoid='+ geoid + '&x=' + longitude + '&y=' + latitude) #just a sample coordinate
	driver.execute_script("window.scrollTo(0, window.scrollY + 10)")

	WebDriverWait(driver, 10)
	driver.save_screenshot("./save/screenshot.png")

	attributes = ['bgroup', 'ct', 'city', 'zipcode', 'neighborhood', 'county']
	write_head = ""

	for attr in attributes:
		elementval = driver.find_element_by_id(attr).text
		if attr == 'bgroup':
			write_head = "Block Group: "
		elif attr == 'ct':
			write_head = "Census Tract: "
		elif attr == 'city':
			write_head = "City: "
		elif attr == 'zipcode':
			write_head = "Zipcode: "
		elif attr == 'neighborhood':
			write_head = "Neighborhood: "
		elif attr == 'county':
			write_head = "County: "
		if elementval is '':
			elementval = write_head + "N/A"
		else:
			print(elementval)
			elementval = write_head + elementval
		row.append(elementval)


	driver.close()

	rows = []
	rows.append(row)

	with open('./save/people.csv', 'w') as writeFile:
		writer = csv.writer(writeFile)
		writer.writerows(rows)

	test_image = "./save/screenshot.png"
	original = Image.open(test_image)

	width, height = original.size   # Get dimensions
	left = 0
	top = 2*height/5
	right = width/2-180
	bottom = height
	cropped_example = original.crop((left, top, right, bottom))

	cropped_example.show()


if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("Usage: python3 screenshot.py [latitude] [longitude]")
		exit()
	latitude = sys.argv[1]
	longitude = sys.argv[2]
	main(latitude, longitude)
