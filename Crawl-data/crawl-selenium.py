import numpy as np
from selenium import webdriver
from time import sleep
import random
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
import pandas as pd
import os, time
# Declare browser

if __name__ == "__main__":

    
    #url_file_driver = os.path.join('etc', 'chromedriver.exe')
    
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)

    #driver = webdriver.Chrome(executable_path = url_file_driver)

    # Open URL
    driver.get("https://www.thegioididong.com/dtdd#c=42&o=9&pi=1")
    #sleep(random.randint(5,10))
    #driver.close()

    # ================================ GET link/title
    #elementName = driver.find_elements(By.XPATH, "./html/body/div[6]/section/div[3]/ul/li[1]/a[1]")
    #title = [elem.text for elem in elementName]
    #elems = driver.find_elements(By.CSS_SELECTOR , "#categoryPage")
    #title = [elem.text for elem in elems]
    #print(title)
    #links = [elem.get_attribute('href') for elem in elems]

    elems = driver.find_elements(By.CSS_SELECTOR , ".listproduct")
    title = [elem.text for elem in elems]
    links = [elem.get_attribute('href') for elem in elems]
    print(title, links)
    
    #driver.switch_to.frame()
    #target = driver.fi