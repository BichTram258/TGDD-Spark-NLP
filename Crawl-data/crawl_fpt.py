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

chromedriver_path = r"C:\Users\HP\chromedriver"

# Khởi tạo trình điều khiển
driver = webdriver.Chrome(executable_path=chromedriver_path)

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
# specifications = [elem.text for elem in elems_specifications]
# print(specifications)
# df_overview_column = ["total", "fiveStar", "rating"]
# overview = [[comment_count[0][0], five_star[0], evaluate[0]]]
# df_overviews = pd.DataFrame(overview, columns=df_overview_column)
# print(df_overviews)
elems_specification = driver.find_elements_by_css_selector(".g-container .l-pd-body__wrapper .l-pd-body__right .card-body .st-pd-table")
A = []
B = []

# Lặp qua các phần tử <table>
for table_element in elems_specification:
    td_elements = table_element.find_elements_by_tag_name('td')
    for i in range(0, len(td_elements), 2):
        if i+1 < len(td_elements):
            A.append(td_elements[i].text)
            B.append(td_elements[i+1].text)

print(A)
print(B)








# values = []
# details = []

# for item in specifications:
#     parts = item.split('\n')
#     for part in parts:
#         if len(part) > 0:
#             split_index = part.index(' ')
#             if not part[split_index+1:].isdigit():
#                 values.append(part)
#                 details.append('')
#             else:
#                 digit_index = split_index + 1
#                 for i, c in enumerate(part[digit_index:]):
#                     if not c.isdigit():
#                         digit_index += i
#                         break
#                 values.append(part[:digit_index])
#                 details.append(part[digit_index:])

# # Tạo DataFrame
# print(values)
# print(details)
# df = pd.DataFrame({'value': values, 'detail': details})
# print(df)

# df = pd.DataFrame(columns = ['Name_phone','Id_comment','Name_comment', 'Buy_place_comment','Content_comment', 'Used_comment'])
# comment = []
# S = 0
# while True:
#     elems_comment = driver.find_elements(By.CSS_SELECTOR , "#root-review .user-content .user-wrapper .user-block .avatar-info .avatar-para")
#     comment = [elem.text for elem in elems_comment] + comment

#     try:       
#         next_page_comment = driver.find_element(By.CSS_SELECTOR, "#root-review .pages .select-device__pagination .pagination.pagination-space .pagination-item .pagination-link .cm-ic-angle-right").click()
#     except:
#         print(comment)
#         break
#     sleep(random.randint(1,3))
# df2 = pd.DataFrame(list(zip(comment)), columns = ['Content_comment'])
#     # df2['link_item'] = links[0]
# df2.insert(0, "Name_phone", Name_Phone[0]) 
# #df2.insert(0) 
# #df2.append(df)
# df = pd.concat([df, df2])
# print(df)


