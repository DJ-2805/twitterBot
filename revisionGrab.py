import urllib.request
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from PIL import Image


def grabBlockImage(url,geoid):
    driver = webdriver.Firefox(executable_path=r'/home/dja/Documents/projects/ITS/masterTwitterBot/resources/geckodriver')

    driver.maximize_window()
    driver.get(url)
    driver.execute_script("window.scrollTo(0, window.scrollY + 10)")

    WebDriverWait(driver, 10)
	driver.save_screenshot("./tweets/"+geoid+".png")

    driver.close()
    return

def clipBlockImage(geoid):
	original = Image.open(geoid+'.png')

	width, height = original.size
	left = 0
	top = 2*height/5
	right = width/2-180
	bottom = height
	cropped = original.crop((left, top, right, bottom))
    return
