#To execute this file, one needs to install selenium by: pip3 install selenium
#Furthermore, one needs to download chromedriver. See https://sites.google.com/a/chromium.org/chromedriver/downloads
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import sys
 
def main(latitude, longitude): 
	options = webdriver.ChromeOptions()
	options.add_argument('--ignore-certificate-errors')
	options.add_argument("--test-type")
	options.binary_location = "/usr/bin/chromium"
	driver = webdriver.Chrome('...') #replace ... with a proper path to the chromedriver
	driver.maximize_window()
	 
	driver.get('http://revision.lewis.ucla.edu/details/index.html?geoid=15000US060372699031&x=' + longitude + '&y=' + latitude) #just a sample coordinate
	driver.execute_script("window.scrollTo(0, window.scrollY + 10)")

	WebDriverWait(driver, 10)
	driver.save_screenshot("screenshot.png")
	 
	driver.close()

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("Usage: python3 screenshot.py [latitude] [longitude]")
		exit()
	latitude = sys.argv[1]
	longitude = sys.argv[2]
	main(latitude, longitude)