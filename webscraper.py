from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
import json
import pandas as pd
import numpy as np
import re
import selenium
import requests,os,sys,math,logging
from selenium.common.exceptions import NoSuchElementException

#logger configs
dirname = os.path.dirname(__file__)
lucky_log_dir = os.path.join(os.path.dirname(__file__),"web.txt")

logging.basicConfig(filename=lucky_log_dir ,filemode="w",format='[TIME: %(asctime)s] [delino@scraper] %(levelname)s: %(message)s', level=logging.INFO) #filename='Practices/log.log',
LOGGER = logging.getLogger("delino@scraper")

#logger func to call
def syslogger(msg, sev = "info"):
    if "debug" in sev :
        LOGGER.debug(msg)        
    elif "info" in sev :
        LOGGER.info(msg)
    elif "warning" in sev :
        LOGGER.warning(msg)
    elif "error" in sev :
        LOGGER.error(msg)
    elif "critical" in sev :
        LOGGER.critical(msg)
    else:
        pass

#config selenium browser and settings
opt = Options()
opt.headless = True
driver = webdriver.Chrome(options=opt) #options=opt
driver.implicitly_wait(7)
driver.maximize_window()

#start browsing with selenium
myurl = "https://www.delino.com/"
driver.get(myurl)
syslogger(f"getting to {myurl}")
driver.implicitly_wait(10)
syslogger("implicit wait set 10 sec!")

##clicking on hamedan as selected city
city_xpath_helper = { "tehran" : "1" , 
                      "qom" : "2" ,
                      "bandar" : "3" ,
                      "karaj" : "4" ,
                      "rasht" : "5" ,
                      "gorgan" : "6" ,
                      "hamedan" : "7" ,
                      "yazd" : "8" ,
                      "urumia" : "9" ,
                      "gonbad" : "10" ,
                      "arak" : "11" ,
                      }

city_xpath = f"/html/body/div[2]/section/div/div[2]/div/section/div/ul/li[{city_xpath_helper['arak']}]"
driver.find_element(by=By.XPATH,value=city_xpath).click()
syslogger(f"clicking on {city_xpath} in wellcome page.")

## going to full restraunts lists
show_all_rests_xpath = "/html/body/div[2]/div[3]/div/div[4]/div[1]/section/div/header/h3/a"
sleep(2)
driver.execute_script("window.scrollBy(0,1000)")
driver.find_element(by=By.XPATH,value=show_all_rests_xpath).click()
syslogger(f"clicking on show all restraunts with xpath : {show_all_rests_xpath}")

## list of restraunts of city
sleep(2)
driver.execute_script("window.scrollBy(0,600)")
elements_of_rest = driver.find_elements(by=By.XPATH,value="/html/body/div[2]/div[3]/div/div[3]/div/div[3]/a")
rest_numbers = len(elements_of_rest)
syslogger(f"number of restraunts in city num {city_xpath_helper['bandar']} is {rest_numbers} ")
driver.execute_script("window.scrollBy(0,-600)")
main_url = driver.current_url
city_data_dict = {}

for ii in range( 1 , rest_numbers+1 ):
    name_list = []
    rates_list = []
    avg_arrival = []
    addr_str_list = []
    addr_lat_long_list = []
    out_of_zone_delivery = []
    avail_time_list = []
    restraunts_menu_list = []
    menu_list_food_data_struct = { "name":"" , "price":"" , "primarythings":"" , "discount":"" , }
    tmp_xapth = f"/html/body/div[2]/div[3]/div/div[3]/div/div[3]/a[{ii}]/section/div/aside/h3"
    try:        
        tmp_name = driver.find_element(by=By.XPATH,value=tmp_xapth).text
        name_list.append(tmp_name)
        syslogger(f"restraunt number {ii} is {tmp_name} .")
        driver.find_element(by=By.XPATH,value=tmp_xapth).click()
        rest_first_page = driver.current_url
        try:
            
            ## getting rate and append in rate list
            rate_xpath = "/html/body/div[2]/div[3]/div/div/div[1]/div[2]/div/aside/div[1]/div[1]/div/b"
            rate_ = driver.find_element(by=By.XPATH,value=rate_xpath).text
            rates_list.append(rate_)
            
            ## gett delivery average and append in avg_arrival
            delivery_avg_xpath = "/html/body/div[2]/div[3]/div/div/div[1]/div[2]/div/aside/div[2]/div[2]/div[1]/b"
            delivery_ = driver.find_element(by=By.XPATH,value=delivery_avg_xpath).text
            avg_arrival.append(delivery_)
            
            ## getting menu with data structure mentioned before
            num_of_menu_parts_xpath = "/html/body/div[2]/div[3]/div/div/div[2]/div/div[2]/div[2]/div[2]/div[1]/section"
            sleep(1)
            num_of_menu_parts = len(driver.find_elements(by = By.XPATH, value = num_of_menu_parts_xpath))
            if (num_of_menu_parts > 0) :
                syslogger(f"menu number is {num_of_menu_parts}")
                print(f"menu number is {num_of_menu_parts}")
            sleep(1)
            for i in range(1 , num_of_menu_parts+1):
                num_of_menu_parts_food_xpath = f"/html/body/div[2]/div[3]/div/div/div[2]/div/div[2]/div[2]/div[2]/div[1]/section[{i}]/div/div/div"
                sleep(1)
                num_of_menu_parts_food = len(driver.find_elements(by = By.XPATH, value = num_of_menu_parts_food_xpath))
                if  (num_of_menu_parts_food > 0) :
                    syslogger(f"menu number is and {num_of_menu_parts_food}")
                    print(f"menu number is and {num_of_menu_parts_food}")
                driver.execute_script(f"window.scrollBy(0,300);")
                for j in range( 1, num_of_menu_parts_food +1):
                    menu_list_food_data_struct1 = menu_list_food_data_struct.copy()
                    
                    food_name_xpath = f"/html/body/div[2]/div[3]/div/div/div[2]/div/div[2]/div[2]/div[2]/div[1]/section[{i}]/div/div/div[{j}]/section/div[2]/h3"
                    sleep(0.5)
                    food_name = driver.find_element(by=By.XPATH,value=food_name_xpath).text
                    
                    primary_things_xpath = f"/html/body/div[2]/div[3]/div/div/div[2]/div/div[2]/div[2]/div[2]/div[1]/section[{i}]/div/div/div[{j}]/section/div[2]/div[1]" 
                    #sleep(1)
                    primary_things = driver.find_element(by=By.XPATH,value=primary_things_xpath).text
                    
                    price_food_xpath = f"/html/body/div[2]/div[3]/div/div/div[2]/div/div[2]/div[2]/div[2]/div[1]/section[{i}]/div/div/div[{j}]/section/div[2]/span/small"
                    sleep(0.5)
                    price_food = driver.find_element(by=By.XPATH,value=price_food_xpath).text
                    
                    discount_xpath = f"/html/body/div[2]/div[3]/div/div/div[2]/div/div[2]/div[2]/div[2]/div[1]/section[{i}]/div/div/div[{j}]/section/div[1]/div/b"
                    #sleep(1)
                    if driver.find_element(by=By.XPATH,value=discount_xpath).is_displayed():
                        discount_percent = driver.find_element(by=By.XPATH,value=discount_xpath)
                    else:
                        discount_percent = "0"
                        
                    menu_list_food_data_struct1["name"] = food_name
                    menu_list_food_data_struct1["price"] = price_food
                    menu_list_food_data_struct1["primarythings"] = primary_things
                    menu_list_food_data_struct1["discount"] = getattr(discount_percent,'text','0')
                    restraunts_menu_list.append(menu_list_food_data_struct1)
                    # driver.execute_script(f"window.scrollBy(0,50);")
                driver.execute_script(f"window.scrollBy(0,1000);")
            syslogger("menu ended ")
            print("menu ended ")
            
            ## clicking to go in full info page
            sleep(1.5)
            driver.get(rest_first_page)
            driver.execute_script(f"window.scrollBy(0,-50000);")
            click_full_info_xpath = "/html/body/div[2]/div[3]/div/div/div[2]/div/div[1]/div[1]/ul/li[3]/a"
            driver.find_element(by=By.XPATH,value=click_full_info_xpath).click()
            print("click full info")
            
            ## getting out of zone availability
            out_of_zone_xpath = "/html/body/div[2]/div[3]/div/div/div[2]/div/div[4]/div/div/section[2]/ul/li[2]/aside"
            out_zone_avail = driver.find_element(by=By.XPATH,value=out_of_zone_xpath).text
            
            ## getting available time 
            time_avail_xpath = "/html/body/div[2]/div[3]/div/div/div[2]/div/div[4]/div/div/section[3]/table" #"/html/body/div[2]/div[3]/div/div/div[2]/div/div[4]/div/div/section[3]/div/ul/li/div/span"
            if driver.find_element(by=By.XPATH,value=time_avail_xpath).is_displayed():
                time_avail = driver.find_element(by=By.XPATH,value=time_avail_xpath).text
            else:
                time_avail = "None"
            
            ## getting full address and lat & long location
            str_addr_xpath = "/html/body/div[2]/div[3]/div/div/div[2]/div/div[4]/div/div/section[1]/div/header/span"
            locater_xpath = "/html/body/div[2]/div[3]/div/div/div[2]/div/div[4]/div/div/section[1]/div/div/div"
            str_addr = driver.find_element(by=By.XPATH,value=str_addr_xpath).text
            locater_style_attr = driver.find_element(by=By.XPATH,value=locater_xpath).get_attribute("style").split(sep="|")
            locater = locater_style_attr[1][:-3]
            sleep(1.5)
            driver.get(main_url)
        except NoSuchElementException as e :
            syslogger(f"Error_index_{ii}_not_found\n{e}")
            name_list.append(f"Error_index_{ii}_not_found")    
        
    except NoSuchElementException as e :
        syslogger(f"Error_index_{ii}_not_found\n{e}")
        name_list.append(f"Error_index_{ii}_not_found")
    city_data_dict[f"{ii}"] = { "name" : tmp_name, "rate" : rate_, "delivery" : delivery_, "menu":restraunts_menu_list, "out_of_zone_available" : out_zone_avail, "time_available" : time_avail, "address_by_str" : str_addr, "address_by_geo":locater, }
print(city_data_dict)
a = json.dumps(city_data_dict)
with open("arak_data.json","w") as jlo:
    jlo.write(a)
syslogger("getting out of browser, BYE")
driver.quit()


hamedan_df = pd.read_json("arak_data.json")
hamedan_df.transpose().to_csv("arak.csv")