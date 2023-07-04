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

def crawler_fpt():
    driver.get("https://fptshop.com.vn/dien-thoai")
    time.sleep(2)

    #=======================================================
    # elems_more_phone = driver.find_elements(By.CSS_SELECTOR , ".cdt-product--loadmore .btn.btn-light")
    # Links_Phone = [elem.get_attribute('href') for elem in elems_more_phone]
    # print(Links_Phone)
    button = driver.find_element(By.CSS_SELECTOR , ".cdt-product--loadmore .btn.btn-light")
    button.click()

    elems_name = driver.find_elements(By.CSS_SELECTOR , ".cdt-product__info h3")
    Name_Phone = [elem.text for elem in elems_name]
    #print(Name_Phone)

    elems_link = driver.find_elements(By.CSS_SELECTOR , ".cdt-product__info h3 .cdt-product__name")
    Links_Phone = [elem.get_attribute('href') for elem in elems_link]
    # time.sleep(10)
    #print(Links_Phone)

    driver.get(Links_Phone[1])
    elems_comment_count = driver.find_elements(By.CSS_SELECTOR , ".st-rating__link #re-rate")
    comment_count = [elem.text.split(" ") for elem in elems_comment_count]

    elems_evaluate = driver.find_elements(By.CSS_SELECTOR, "#root-review .fpt-comment .f-s-ui-44.text-primary.f-w-500.m-t-4")
    evaluate = [elem.text for elem in elems_evaluate]

    elems_five_star = driver.find_elements(By.CSS_SELECTOR, "#root-review .fpt-comment .user-rate__box .row .col-4 .progress-block__line .text.m-l-4")
    five_star = [elem.text for elem in elems_five_star]

    elems_specifications = driver.find_elements(By.CSS_SELECTOR, ".g-container .l-pd-body__wrapper .l-pd-body__right .card-body .st-pd-table")
    specifications = [elem.text for elem in elems_specifications]
    print(evaluate)
    print(comment_count)
    print(five_star)
    print(specifications)
    df_overview_column = ["total", "fiveStar", "rating"]
    overview = [[comment_count[0][0], five_star[0], evaluate[0]]]
    print(overview)
    df_overviews = pd.DataFrame(overview, columns=df_overview_column)
    return df_overviews


if __name__ == "__main__":

    
    chromedriver_path = r"C:\Users\HP\chromedriver"

    # Khởi tạo trình điều khiển
    driver = webdriver.Chrome(executable_path=chromedriver_path)
    driver.get("https://www.thegioididong.com/dtdd/samsung-galaxy-z-fold4")
   

    # ================================GET ALL COMMENT IN PAGE 1=================================== 
    elems_name = driver.find_elements(By.CSS_SELECTOR , ".detail h1")
    Name_Phone = [elem.text for elem in elems_name]
    #print(Name_Phone)
    # df = pd.DataFrame(columns = ['Name_phone','Id_comment','Name_comment', 'Buy_place_comment','Content_comment', 'Used_comment'])
    df = pd.DataFrame(columns = ['Content_comment'])
    
    elems_comment_link = driver.find_elements(By.CSS_SELECTOR , ".box-border .comment-btn .comment-btn__item.right-arrow")
    comment_link = [elem.get_attribute('href') for elem in elems_comment_link]
    driver.get(comment_link[0])
  
    elems_comment_count = driver.find_elements(By.CSS_SELECTOR , "#hdfRatingAmount")
    comment_count = [elem.get_attribute('value') for elem in elems_comment_count]
    #print(comment_count[0])

    S = 0
    
    comment_id, comment_name, comment_buy_place, comment, comment_used = [], [], [], [], []


    # ================================ next pagination page end
    
    if int(comment_count[0]) > 120:
        try:
            driver.find_element("xpath", "/html/body/section[1]/div[4]/div[8]/div/a[4]").click()
        except:
            driver.find_element("xpath", "/html/body/section[1]/div[4]/div[7]/div/a[4]").click()
    elif int(comment_count[0]) > 90 and int(comment_count[0]) <=120:
        try:
            driver.find_element("xpath", "/html/body/section[1]/div[4]/div[8]/div/a[3]").click()
        except:
            driver.find_element("xpath", "/html/body/section[1]/div[4]/div[7]/div/a[3]").click()
    elif int(comment_count[0]) > 60 and int(comment_count[0]) <= 90:
        try:
            driver.find_element("xpath", "/html/body/section[1]/div[4]/div[8]/div/a[2]").click()
        except:
            driver.find_element("xpath", "/html/body/section[1]/div[4]/div[7]/div/a[2]").click()
    elif int(comment_count[0]) > 30 and int(comment_count[0]) <= 60:
        try:
            driver.find_element("xpath", "/html/body/section[1]/div[4]/div[8]/div/a[1]").click()
        except:
            driver.find_element("xpath", "/html/body/section[1]/div[4]/div[7]/div/a[1]").click()
    else: 
        pass

    while True:

        #================================ GET comment-id
        elems_comment_id = driver.find_elements(By.CSS_SELECTOR , ".comment.comment--all.ratingLst .comment__item.par")
        comment_id = [elem.get_attribute('id') for elem in elems_comment_id] + comment_id

        #================================ GET comment-name
        elems_comment_name = driver.find_elements(By.CSS_SELECTOR , ".comment.comment--all.ratingLst .comment__item.par .txtname")
        comment_name = [elem.text for elem in elems_comment_name] + comment_name

        #================================ GET comment-place
        elems_comment_buy_place = driver.find_elements(By.CSS_SELECTOR , ".comment.comment--all.ratingLst .comment__item.par .tickbuy")
        comment_buy_place = [elem.text for elem in elems_comment_buy_place] + comment_buy_place
                
        #================================ GET comment
        elems_comment = driver.find_elements(By.CSS_SELECTOR , ".comment.comment--all.ratingLst .comment__item.par .comment-content .cmt-txt")
        comment = [elem.text for elem in elems_comment] + comment
                
        #================================ GET comment-used
        elems_comment_used = driver.find_elements(By.CSS_SELECTOR , ".comment__item.par .item-click .click-use")
        comment_used = [elem.text for elem in elems_comment_used] + comment_used

        S = len(comment_name)
        #print(S)        
        if S != int(comment_count[0]):
            try:
                #print(comment_count[0])
            # ================================ next pagination        
                driver.find_element("xpath", "/html/body/section[1]/div[4]/div[8]/div/a[1]").click()
            except:
                driver.find_element("xpath", "/html/body/section[1]/div[4]/div[7]/div/a[1]").click()
            #print("Clicked on button next page!")
        else:
            break
        sleep(random.randint(1,3))
        #count += 1
        


    df2 = pd.DataFrame(list(zip(comment)), columns = ['Content_comment'])
        # df2['link_item'] = links[0]
    #df2.insert(0, "Name_phone", Name_Phone[0]) 
    #df2.insert(0) 
    #df2.append(df)
    df = pd.concat([df, df2])
    print(df)
    # df.to_excel(r'E:\TGDD-Spark-NLP\tgdd_excel.xlsx', index=False)
    # df.to_csv(r'E:\TGDD-Spark-NLP\tgdd_csv.xlsx', index=False)
    df.to_json(r'E:\TGDD-Spark-NLP\tgdd_json.xlsx', orient='records')
    