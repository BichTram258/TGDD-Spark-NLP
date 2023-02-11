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

    
    #url_file_driver = os.path.join('etc', 'chromedriver.exe')
    
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)

    #wait = WebDriverWait(driver,10)

    #driver.maximize_window()
    #driver = webdriver.Chrome(executable_path = url_file_driver)

    # Open URL
    driver.get("https://www.thegioididong.com/dtdd#c=42&o=9&pi=1")
    #sleep(random.randint(5,10))
    #driver.close()


    #================================ GET name phone
    elems_name = driver.find_elements(By.CSS_SELECTOR , ".listproduct h3")
    Name_Phone = [elem.text for elem in elems_name]
    #print(Name_Phone)
    
    #================================ GET link phone
    elems_link = driver.find_elements(By.CSS_SELECTOR , ".listproduct .main-contain")
    Links_Phone = [elem.get_attribute('href') for elem in elems_link]
    #print(Links_Phone)

    #================================ GET price phone
    elems_price = driver.find_elements(By.CSS_SELECTOR , ".listproduct .price")
    len(elems_price)
    Price_Phone = [elem_price.text for elem_price in elems_price]
    #print(Price_Phone)

    #================================ GET df1 all 1 page Phone
    df1 = pd.DataFrame(list(zip(Name_Phone, Links_Phone, Price_Phone)), columns = ['title', 'link','price'])
    df1['index_']= np.arange(1, len(df1) + 1)
    #print(df1)


    # GET MORE INFOR OF EACH ITEM 
    #driver.get(Links_Phone[6])
    #sleep(random.randint(5,10))

    #================================ GET comment-link
    elems_comment_link = driver.find_elements(By.CSS_SELECTOR , ".box-border .comment-btn .comment-btn__item.right-arrow")
    comment_link = [elem.get_attribute('href') for elem in elems_comment_link]
    #print(comment_link)
    #print(len(comment_link))

    # GET MORE INFOR OF COMMENT
    #driver.get(comment_link[0])

    #sleep(6)


    # ================================GET ALL COMMENT IN PAGE 1=================================== 
    count = 0
    
    df = pd.DataFrame(columns = ['Name_phone','Id_comment','Name_comment', 'Buy_place_comment','Content_comment', 'Used_comment'])
  
    while True:
        try:
            print("Crawl smartphone " + str(Name_Phone[count]))
            driver.get(Links_Phone[count])
            #print(Links_Phone[count])
            elems_comment_link = driver.find_elements(By.CSS_SELECTOR , ".box-border .comment-btn .comment-btn__item.right-arrow")
            comment_link = [elem.get_attribute('href') for elem in elems_comment_link]


            elems_comment_count = driver.find_elements(By.CSS_SELECTOR , "#hdfRatingAmount")
            comment_count = [elem.get_attribute('value') for elem in elems_comment_count]
            #print(comment_count[0])

            if len(comment_link) == 0:
                count += 1 
                continue
            
            else:
                    
                driver.get(comment_link[0])
                #print(comment_link[0])
                #count = 1
                S = 0
                
                comment_id, comment_name, comment_buy_place, comment, comment_used = [], [], [], [], []

                # ================================ next pagination page end
                
                if int(comment_count[0]) > 120:
                    driver.find_element("xpath", "/html/body/section[1]/div[4]/div[8]/div/a[4]").click()
                elif int(comment_count[0]) > 90 and int(comment_count[0]) <=120:
                    driver.find_element("xpath", "/html/body/section[1]/div[4]/div[8]/div/a[3]").click()
                elif int(comment_count[0]) > 60 and int(comment_count[0]) <= 90:
                    driver.find_element("xpath", "/html/body/section[1]/div[4]/div[8]/div/a[2]").click()
                elif int(comment_count[0]) > 30 and int(comment_count[0]) <= 60:
                    try:
                        driver.find_element("xpath", "/html/body/section[1]/div[4]/div[8]/div/a[1]").click()
                    except:
                        driver.find_element("xpath", "/html/body/section[1]/div[4]/div[7]/div/a[1]").click()
                else: 
                    pass

                while True:
                                
                    #print("Crawl Page " + str(count))

                    elems_comment_count = driver.find_elements(By.CSS_SELECTOR , "#hdfRatingAmount")
                    comment_count = [elem.get_attribute('value') for elem in elems_comment_count]

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
                    
            
            
                df2 = pd.DataFrame(list(zip( comment_id, comment_name , comment_buy_place, comment, comment_used)), columns = ['Id_comment','Name_comment', 'Buy_place_comment','Content_comment', 'Used_comment'])
                    # df2['link_item'] = links[0]
                df2.insert(0, "Name_phone", Name_Phone[count]) 
                #df2.insert(0) 
                #df2.append(df)
                df = pd.concat([df, df2])
                print(df) 
             
                
                
                
            count += 1 

        
        except:
            print("Element Not Interactable Exception!")
            export_csv = df.to_csv (r'C:\Users\TRAM\TGDD-Setiment-Analysis\Crawl-data\data-comment\data.csv', index = None, header=True)
            break
        

        
        
    # Close browser
    #driver.close()    
#====================================================FOR EXAMPLE=============================================
#=========IN PAGE 1
# page 7 /html/body/section[1]/div[4]/div[8]/div/a[4]________________________________________________________ << /html/body/section[1]/div[4]/div[8]/div/a[4]
# page 2 /html/body/section[1]/div[4]/div[8]/div/a[5]______/html/body/section[1]/div[4]/div[8]/div/a[1]______ >> /html/body/section[1]/div[4]/div[8]/div/a[1]  /html/body/section[1]/div[4]/div[8]/div/a[5] 

#=========IN PAGE 2 
# page 1 /html/body/section[1]/div[4]/div[8]/div/a[1]______/html/body/section[1]/div[4]/div[8]/div/a[2]______ <<  /html/body/section[1]/div[4]/div[8]/div/a[1] /html/body/section[1]/div[4]/div[8]/div/a[2]
# page 3 /html/body/section[1]/div[4]/div[8]/div/a[6]______/html/body/section[1]/div[4]/div[8]/div/a[3]______ >>  
#=========IN PAGE 3
# page 2 /html/body/section[1]/div[4]/div[8]/div/a[1]______/html/body/section[1]/div[4]/div[8]/div/a[3]______ <<  
# page 4 /html/body/section[1]/div[4]/div[8]/div/a[6]______/html/body/section[1]/div[4]/div[8]/div/a[4]______ >> 
#=========IN PAGE 4
# page 3 /html/body/section[1]/div[4]/div[8]/div/a[1]______/html/body/section[1]/div[4]/div[8]/div/a[3]______ << 
#=========IN PAGE 5
# page 4 /html/body/section[1]/div[4]/div[8]/div/a[1]______/html/body/section[1]/div[4]/div[8]/div/a[3]______ <<
# page 6 /html/body/section[1]/div[4]/div[8]/div/a[6]______/html/body/section[1]/div[4]/div[8]/div/a[4]______ >>
#=========IN PAGE 6
# page 5 /html/body/section[1]/div[4]/div[8]/div/a[1]______/html/body/section[1]/div[4]/div[8]/div/a[4]______ << 
# page 7 __________________________________________________/html/body/section[1]/div[4]/div[8]/div/a[5]______ >>
#=========IN PAGE 7
# page 6 /html/body/section[1]/div[4]/div[8]/div/a[1]______/html/body/section[1]/div[4]/div[8]/div/a[5]______ <<  
#____________________________________________________________________________________________________________@
# page 7 /html/body/section[1]/div[4]/div[8]/div/a[4]