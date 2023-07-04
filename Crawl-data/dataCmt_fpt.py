import numpy as np
from selenium import webdriver
from time import sleep
import random
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from pandas import DataFrame
import csv
import os, time
# Declare browser


if __name__ == "__main__":

    
    chromedriver_path = r"C:\Users\HP\chromedriver"

    # Khởi tạo trình điều khiển
    driver = webdriver.Chrome(executable_path=chromedriver_path)
    driver.get("https://fptshop.com.vn/dien-thoai")
    sleep(random.randint(2, 4))
    #driver.close()


    button = driver.find_element(By.CSS_SELECTOR , ".cdt-product--loadmore .btn.btn-light")
    button.click()

    elems_name = driver.find_elements(By.CSS_SELECTOR , ".cdt-product__info h3")
    Name_Phone = [elem.text for elem in elems_name]
    #print(Name_Phone)

    elems_link = driver.find_elements(By.CSS_SELECTOR , ".cdt-product__info h3 .cdt-product__name")
    Links_Phone = [elem.get_attribute('href') for elem in elems_link]
    
    link_dict_fpt = {name: link for name, link in zip(Name_Phone, Links_Phone)}

    # In liên kết tương ứng của một phần tử trong mảng 1
    # nối với database để lấy tên điện thoại
    item = 'Samsung Galaxy A34 5G'
    while True:
        if link_dict_fpt[item]:
            driver.get(link_dict_fpt[item])
            time.sleep(3)
            comment = []
            while True:
                    elems_comment = driver.find_elements(By.CSS_SELECTOR , "#root-review .fpt-comment .user-content .user-wrapper .user-block .avatar.avatar-md.avatar-text.avatar-circle .avatar-info .avatar-para")
                    comment += [elem.text for elem in elems_comment if "reply" not in elem.get_attribute("class")] 
                    try:
                        driver.find_element(By.CSS_SELECTOR, "#root-review .fpt-comment .pages .select-device__pagination .pagination.pagination-space .pagination-item .pagination-link .cm-ic-angle-right").click()
                        time.sleep(3)
                    except:
                        break
            df_data = pd.DataFrame({"comment": comment})
            print(df_data)
            break
        
        else:
            pass
   
    

    