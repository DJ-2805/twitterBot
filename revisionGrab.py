import urllib.request
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from PIL import Image

path = r'/home/itsadmin/Documents/twitterBot/resources/geckodriver'

def grabBlockImage(blocks):
    driver = webdriver.Firefox(executable_path=path)
    driver.maximize_window()

    size = blocks.shape[0]

    for i in range(5):
        geoid = str(blocks['GeoID'][i])
        url = blocks['Link'][i]
        driver.get(url)
        driver.execute_script("window.scrollTo(0, window.scrollY + 10)")
        WebDriverWait(driver, 10)
        driver.save_screenshot("./tweets/"+geoid+".png")

    driver.close()

def clipBlockImage(geoid):
	original = Image.open(geoid+'.png')

	width, height = original.size
	left = 0
	top = 2*height/5
	right = width/2-180
	bottom = height
	cropped = original.crop((left, top, right, bottom))
