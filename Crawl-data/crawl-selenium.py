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

    #================================ GET name
    elems_name = driver.find_elements(By.CSS_SELECTOR , ".listproduct h3")
    Name_Phone = [elem.text for elem in elems_name]
    #print(Name_Phone)
    
    #================================ GET link
    elems_link = driver.find_elements(By.CSS_SELECTOR , ".listproduct .main-contain")
    Links_Phone = [elem.get_attribute('href') for elem in elems_link]
    #print(Links_Phone)

    #================================ GET price
    elems_price = driver.find_elements(By.CSS_SELECTOR , ".listproduct .price")
    len(elems_price)
    Price_Phone = [elem_price.text for elem_price in elems_price]
    #print(Price_Phone)

    #================================ GET df1
    df1 = pd.DataFrame(list(zip(Name_Phone, Links_Phone, Price_Phone)), columns = ['title', 'link','price'])
    df1['index_']= np.arange(1, len(df1) + 1)
    #print(df1)

    #elems_countReviews = driver.find_elements(By.CSS_SELECTOR , ".listproduct .item-rating-total")
    #countReviews = [elem.text for elem in elems_countReviews]
    #print(countReviews)

    #df1['countReviews'] = countReviews
    #df2 = pd.DataFrame(list(zip(countReviews)), columns = ['reviews'])
    #df1['countReviews'] = countReviews
    #df1['countReviews']=df1['countReviews'].astype(int)
    #df3 = df1.merge(df2, how='left', left_on='index_', right_on='reviews')
    #print(df1)
    #driver.switch_to.frame()
    #target = driver.fi

    # ================================ GET more infor of each item 
    driver.get(Links_Phone[0])
    #sleep(random.randint(5,10))

    elems_link_comment = driver.find_elements(By.CSS_SELECTOR , ".box-border .comment-btn")
    Links_comment = [elem.get_attribute('href') for elem in elems_link_comment]
    print(Links_comment)  

    elems_name = driver.find_elements(By.CSS_SELECTOR , ".comment-content")
    name_comment = [elem.text for elem in elems_name]
    #print(name_comment)

    