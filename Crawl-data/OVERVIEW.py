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
import pymongo
# client = pymongo.MongoClient("mongodb+srv://thiendihill181:A0YZHAJ9L4kxZfhb@cluster0.ys2zvmm.mongodb.net/")
# db = client["test"]
# collection = db["phones"]
# Declare browser

if __name__ == "__main__":

    # query = {"$and": [
    #     {"_id": {"$exists": True}},
    #     {"status": "0"}
    # ]}
    # record = collection.find_one(query)
    chromedriver_path = r"C:\Users\HP\chromedriver"

    # Khởi tạo trình điều khiển
    driver = webdriver.Chrome(executable_path=chromedriver_path)
    driver.get("https://www.thegioididong.com/dtdd#c=42&o=17&pi=1")
    time.sleep(2)
    #sleep(random.randint(5,10))
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
    # item = record["name"]
    item = 'Samsung Galaxy Z Flip4 5G'
    comment_count_tgdd, evaluate_tgdd, five_star_tgdd = [], [], []
    while True:
        if link_dict_tgdd[item]:
            driver.get(link_dict_tgdd[item])
            time.sleep(2)
            elems_comment_link = driver.find_elements(By.CSS_SELECTOR , ".box-border .comment-btn .comment-btn__item.right-arrow")
            comment_link = [elem.get_attribute('href') for elem in elems_comment_link]
            driver.get(comment_link[0])
            time.sleep(2)
            
            elems_comment_count_tgdd = driver.find_elements(By.CSS_SELECTOR , "#hdfRatingAmount")
            comment_count_tgdd = [elem.get_attribute('value') for elem in elems_comment_count_tgdd] + comment_count_tgdd
            
            elems_evaluate_tgdd = driver.find_elements(By.CSS_SELECTOR, ".frames-detail .rating-star.rating-viewall .rating-left .point")
            evaluate_tgdd = [elem.text for elem in elems_evaluate_tgdd] + evaluate_tgdd
            
            # cần chú ý đường link, mỗi đt sẽ có mỗi đường link khác nhau
            elems_five_star = driver.find_element_by_xpath("/html/body/section[1]/div[4]/div[3]/a[2]") 
            driver.execute_script("arguments[0].click();", elems_five_star)

            elems_five_star_tgdd = driver.find_elements(By.CSS_SELECTOR, ".clearfix.rtFilter .rating-amount.fleft")
            five_star_tgdd = [elem.text.split(" ") for elem in elems_five_star_tgdd] + five_star_tgdd
            break
        else:
            pass
    driver.get("https://fptshop.com.vn/dien-thoai?sort=ban-chay-nhat&trang=2")
    time.sleep(2)
    elems_qc = driver.find_elements(By.CSS_SELECTOR, ".ins-preview-wrapper.ins-preview-wrapper-4022.ins-pos-middle-center #wrap-close-button-1545222288830 .ins-element-content")
    if elems_qc:
        elems_qc.click()
    
    elems_name_fpt = driver.find_elements(By.CSS_SELECTOR , ".cdt-product__info h3 .cdt-product__name")
    Name_Phone_fpt = [elem.text for elem in elems_name_fpt]
    print(Name_Phone_fpt)

    elems_link_fpt = driver.find_elements(By.CSS_SELECTOR , ".cdt-product__info h3 .cdt-product__name")
    Links_Phone_fpt = [elem.get_attribute('href') for elem in elems_link_fpt]
    
    link_dict_fpt = {name: link for name, link in zip(Name_Phone_fpt, Links_Phone_fpt)}
    
    comment_count_fpt, evaluate_fpt, five_star_fpt = [], [], []
    values = []
    details = []
    item_fpt = 'Samsung Galaxy Z Flip4 5G 128GB'
    
    
    while True: 
        if link_dict_fpt[item_fpt]:
            driver.get(link_dict_fpt[item_fpt])
            time.sleep(2)
            elems_comment_count_fpt = driver.find_elements(By.CSS_SELECTOR , ".st-rating__link #re-rate")
            comment_count_fpt = [elem.text.split(" ") for elem in elems_comment_count_fpt] + comment_count_fpt

            elems_evaluate_fpt = driver.find_elements(By.CSS_SELECTOR, "#root-review .fpt-comment .f-s-ui-44.text-primary.f-w-500.m-t-4")
            evaluate_fpt = [elem.text for elem in elems_evaluate_fpt] + evaluate_fpt

            elems_five_star_fpt = driver.find_elements(By.CSS_SELECTOR, "#root-review .fpt-comment .user-rate__box .row .col-4 .progress-block__line .text.m-l-4")
            five_star_fpt = [elem.text for elem in elems_five_star_fpt] + five_star_fpt
            
            elems_specifications_fpt = driver.find_elements(By.CSS_SELECTOR, ".g-container .l-pd-body__wrapper .l-pd-body__right .card-body .st-pd-table")
            for table_element in elems_specifications_fpt:
                td_elements = table_element.find_elements_by_tag_name('td')
                for i in range(0, len(td_elements), 2):
                    if i+1 < len(td_elements):
                        values.append(td_elements[i].text)
                        details.append(td_elements[i+1].text)
            break

    # In DataFrame
#===============================================LƯU VÀO DB
    df_specification = pd.DataFrame({"values": values, "details": details})
    df_specification = df_specification[["values", "details"]].transpose()
    df_specification.columns = df_specification.iloc[0]
    df_specification = df_specification.iloc[1:].reset_index(drop=True)
    

    if not comment_count_fpt[0][0]:
        comment_count_fpt[0][0] = 0
    if not comment_count_tgdd[0]:
        comment_count_tgdd[0] = 0
    if not five_star_tgdd[0][0]:
        five_star_tgdd[0][0] = 0
    if not five_star_fpt[0]:
        five_star_fpt[0] = 0
    if not evaluate_tgdd[0]:
        evaluate_tgdd[0] = 0
    if not evaluate_fpt[0]:
        evaluate_fpt[0] = 0
    rating_parts = evaluate_fpt[0].split('/')
    overview = [[float(comment_count_fpt[0][0])+float(comment_count_tgdd[0]), float(five_star_tgdd[0][0])+float(five_star_fpt[0]), (float(evaluate_tgdd[0]) + float(rating_parts[0])) / 2]]
    df_overview_column = ["total", "fiveStar", "rating"]
    df_overviews = pd.DataFrame(overview, columns=df_overview_column)
    print(df_specification)
    print(df_overviews)
    
    # data_specification = {
    #     "màn hình": str(df_specification["Màn hình"].item()),
    #     "camera trước": str(df_specification["Camera sau"].item()),
    #     "camera selfie": str(df_specification["Camera Selfie"].item()),
    #     "ram": str(df_specification["RAM"].item()),
    #     "bộ nhớ trong": str(df_specification["Bộ nhớ trong"].item()),
    #     "cpu": str(df_specification["CPU"].item()),
    #     "dung lượng pin": str(df_specification["Dung lượng pin"].item()),
    #     "thẻ sim": str(df_specification["Thẻ sim"].item()),
    #     "hệ điều hành": str(df_specification["Hệ điều hành"].item()),
    #     "xuất xứ": str(df_specification["Xuất xứ"].item()),
    #     "thời gian ra mắt": str(df_specification["Thời gian ra mắt"].item()),
    # }
    # data_overview = {
    #     "tổng bình luận": int(df_overviews["total"].iloc[0]),
    #     "tổng 5 sao": int(df_overviews["fiveStar"].iloc[0]),
    #     "đánh giá": float(df_overviews["rating"].iloc[0])
    # }
    # data_update = {
    #     "overview": data_overview
   
    # }
    # collection.update_one({"_id": record["_id"]}, {"$set": {"overview": data_overview, "specification": data_specification}})

#==============================================================================
    
    

    