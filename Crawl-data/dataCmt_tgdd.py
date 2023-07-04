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
    driver.get("https://www.thegioididong.com/dtdd#c=42&o=17&pi=1")
    sleep(random.randint(2, 4))
    #driver.close()


    #================================ GET name phone
    elems_name_tgdd = driver.find_elements(By.CSS_SELECTOR , ".listproduct h3")
    Name_Phone_tgdd = [elem.text for elem in elems_name_tgdd]
    # print(Name_Phone_tgdd)
    
    #================================ GET link phone
    elems_link_tgdd = driver.find_elements(By.CSS_SELECTOR , ".listproduct .main-contain")
    Links_Phone_tgdd = [elem.get_attribute('href') for elem in elems_link_tgdd]
    # print(Links_Phone_tgdd)
    
    link_dict_tgdd = {name: link for name, link in zip(Name_Phone_tgdd, Links_Phone_tgdd)}

    # In liên kết tương ứng của một phần tử trong mảng 1
    # nối với database để lấy tên điện thoại
    item = 'Samsung Galaxy Z Flip4 5G'
    comment_id, comment_name, comment = [], [], []
    while True:
        if link_dict_tgdd[item]:
            driver.get(link_dict_tgdd[item])
            time.sleep(2)
            elems_comment_link = driver.find_elements(By.CSS_SELECTOR , ".box-border .comment-btn .comment-btn__item.right-arrow")
            comment_link = [elem.get_attribute('href') for elem in elems_comment_link]
            driver.get(comment_link[0])
            time.sleep(2)
            elems_comment_count = driver.find_elements(By.CSS_SELECTOR , "#hdfRatingAmount")
            comment_count = [elem.get_attribute('value') for elem in elems_comment_count]
            if int(comment_count[0]) > 120:
                try:
                    driver.find_element("xpath", "/html/body/section[1]/div[4]/div[8]/div/a[4]").click()
                except:
                    driver.find_element("xpath", "/html/body/section[1]/div[4]/div[7]/div/a[4]").click()
                time.sleep(2)
            elif int(comment_count[0]) > 90 and int(comment_count[0]) <=120:
                try:
                    driver.find_element("xpath", "/html/body/section[1]/div[4]/div[8]/div/a[3]").click()
                except:
                    driver.find_element("xpath", "/html/body/section[1]/div[4]/div[7]/div/a[3]").click()
                time.sleep(2)
            elif int(comment_count[0]) > 60 and int(comment_count[0]) <= 90:
                try:
                    driver.find_element("xpath", "/html/body/section[1]/div[4]/div[8]/div/a[2]").click()
                except:
                    driver.find_element("xpath", "/html/body/section[1]/div[4]/div[7]/div/a[2]").click()
                time.sleep(2)
            elif int(comment_count[0]) > 30 and int(comment_count[0]) <= 60:
                try:
                    driver.find_element("xpath", "/html/body/section[1]/div[4]/div[8]/div/a[1]").click()
                except:
                    driver.find_element("xpath", "/html/body/section[1]/div[4]/div[7]/div/a[1]").click()
                time.sleep(2)
            else: 
                pass
            while True:

                #================================ GET comment-id
                elems_comment_id = driver.find_elements(By.CSS_SELECTOR , ".comment.comment--all.ratingLst .comment__item.par")
                comment_id += [elem.get_attribute('id') for elem in elems_comment_id]

                #================================ GET comment-name
                elems_comment_name = driver.find_elements(By.CSS_SELECTOR , ".comment.comment--all.ratingLst .comment__item.par .txtname")
                comment_name += [elem.text for elem in elems_comment_name] 
                        
                #================================ GET comment
                elems_comment = driver.find_elements(By.CSS_SELECTOR , ".comment.comment--all.ratingLst .comment__item.par .comment-content .cmt-txt")
                comment += [elem.text for elem in elems_comment]

                S = len(comment_id)
                #print(S)        
                if S != int(comment_count[0]):
                    try:
                        #print(comment_count[0])
                    # ================================ next pagination        
                        driver.find_element("xpath", "/html/body/section[1]/div[4]/div[8]/div/a[1]").click()
    
                    except:
                        driver.find_element("xpath", "/html/body/section[1]/div[4]/div[7]/div/a[1]").click()
                    time.sleep(2)
                    #print("Clicked on button next page!")
                else:
                    break
                sleep(random.randint(1,3))
                #count += 1
                
            df_data = pd.DataFrame({"id": comment_id, "name": comment_name, "comment": comment})
            print(df_data)
            break
        else:
            pass
   
    driver.get("https://fptshop.com.vn/dien-thoai?sort=ban-chay-nhat&trang=2")
    sleep(random.randint(2, 4))
    #driver.close()
    button = driver.find_element(By.CSS_SELECTOR , ".cdt-product--loadmore .btn.btn-light")
    button.click()

    elems_name = driver.find_elements(By.CSS_SELECTOR , ".cdt-product__info h3")
    Name_Phone = [elem.text for elem in elems_name]
    print(Name_Phone)

    elems_link = driver.find_elements(By.CSS_SELECTOR , ".cdt-product__info h3 .cdt-product__name")
    Links_Phone = [elem.get_attribute('href') for elem in elems_link]
    
    link_dict_fpt = {name: link for name, link in zip(Name_Phone, Links_Phone)}

    # In liên kết tương ứng của một phần tử trong mảng 1
    # nối với database để lấy tên điện thoại
    item_fpt = 'Samsung Galaxy Z Flip4 5G 128GB'

    while True:
        if link_dict_fpt[item_fpt]:
            driver.get(link_dict_fpt[item_fpt])
            time.sleep(3)
            while True:
                    elems_comment = driver.find_elements(By.CSS_SELECTOR , "#root-review .fpt-comment .user-content .user-wrapper .user-block .avatar.avatar-md.avatar-text.avatar-circle .avatar-info .avatar-para")
                    comment += [elem.text for elem in elems_comment] 
                    try:
                        driver.find_element(By.CSS_SELECTOR, "#root-review .fpt-comment .pages .select-device__pagination .pagination.pagination-space .pagination-item .pagination-link .cm-ic-angle-right").click()
                        time.sleep(3)
                    except:
                        break

            break
        
        else:
            pass
    df_data = pd.DataFrame({"comment": comment})
    print(df_data)
    df_data.to_csv(r'E:\TGDD-Spark-NLP\SamsungZFlip45G128GB.csv', index=False)
    