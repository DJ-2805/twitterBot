#To execute this file, one needs to install selenium by: pip3 install selenium
#Furthermore, one needs to download chromedriver. See https://sites.google.com/a/chromium.org/chromedriver/downloads
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import sys
import os
import time
import csv
 
def main(latitude, longitude):
    directory = "./save"
	if not os.path.exists(directory):
		os.makedirs(directory)
	row = []

	curr_time = time.time()
	options = webdriver.ChromeOptions()
	options.add_argument('--ignore-certificate-errors')
	options.add_argument("--test-type")
	options.binary_location = "/usr/bin/chromium"
        driver = webdriver.Chrome('/usr/lib/chomium-browser/chromedriver') #replace ... with a proper path to the chromedriver
	driver.maximize_window()
	 
	driver.get('http://revision.lewis.ucla.edu/details/index.html?geoid=15000US060372699031&x=' + longitude + '&y=' + latitude) #just a sample coordinate
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
	

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("Usage: python3 screenshot.py [latitude] [longitude]")
		exit()
	latitude = sys.argv[1]
	longitude = sys.argv[2]
	main(latitude, longitude)
