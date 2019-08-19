import urllib.request
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from PIL import Image

path = r'/home/itsadmin/Documents/twitterBot/resources/geckodriver'

def grabBlockImage(blocks,size):
    driver = webdriver.Firefox(executable_path=path)
    driver.maximize_window()

    for i in range(size):
        geoid = str(blocks['GeoID'][i])
        url = blocks['Link'][i]
        driver.get(url)
        driver.execute_script("window.scrollTo(0, window.scrollY + 10)")
        WebDriverWait(driver, 10)
        sleep(5)
        driver.save_screenshot("../screenshots/"+geoid+".png")

    driver.close()

def clipBlockImage(blocks,size):
    for i in range(size):
        geoid = str(blocks['GeoID'][i])
        try:
            original = Image.open('../screenshots/'+geoid+'.png')
            width,height = original.size
            left = 14
            top = 2*height/5 - 78
            right = width/2-310
            bottom = height - 245
            cropped = original.crop((left,top,right,bottom))
            cropped.save('../tweets/'+geoid+'.png','PNG')
        except:
            print(geoid)
