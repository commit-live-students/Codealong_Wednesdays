# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 17:27:15 2020

@author: nnair
"""

# WEB SCRAPING 101

# Header files
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd    



# Function for searching cuisine

def search_cuisine(cuisine_name):
    
    # Finding the search bar
    search_item = driver.find_element_by_class_name("discover-search")
    
    #Input the cuisine
    search_item.send_keys(cuisine_name)    
    driver.find_element_by_id("search_button").click()
    driver.find_element_by_id("search_button").click()

    WebDriverWait(driver, 500).until(lambda driver: driver.find_element_by_class_name("close"))
    driver.find_element_by_class_name("close").click()
#    
#    
#    # Click on the search button
    driver.find_element_by_id("search_button").click()

    return    



# URL to scrape
main_url = "https://www.zomato.com"

# Wait for the window to load


# Launching the web driver
driver = webdriver.Chrome()

driver.implicitly_wait(5)
driver.maximize_window()


# Open the URL
driver.get(main_url)

cuisine_name="Chinese"

print("Searching for " + cuisine_name)

# Calling the function
search_cuisine(cuisine_name)

# Waiting for elements to load
WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath("//*[@class='result-title hover_feedback zred bold ln24   fontsize0 ']"))

# Storing the results in a list
listings = driver.find_elements_by_xpath("//*[@class='result-title hover_feedback zred bold ln24   fontsize0 ']")


# Creating an empty dataframe to store scraped data
df = pd.DataFrame(columns=['Name','cuisine','rating','location','url'])

# Storing the current window
current_window = driver.current_window_handle

for listing in listings: 
    
    # Get the link of restaurant page
    url=listing.get_attribute('href') 

    # Open the URL in a new window                         
    driver.execute_script('window.open(arguments[0]);', url)
    new_window=driver.window_handles[1]
    driver.switch_to.window(new_window)
    
    # Storing restaurant name  
    WebDriverWait(driver, 500).until(lambda driver: driver.find_element_by_xpath("//h1[@class='sc-7kepeu-0 sc-ivVeuv kBFhIT']").text)
    rest_name=driver.find_element_by_xpath("//h1[@class='sc-7kepeu-0 sc-ivVeuv kBFhIT']").text
    
    # Storing restaurant cuisine
    WebDriverWait(driver, 100).until(lambda driver: driver.find_elements_by_xpath("//*[@class='sc-hdPSEv kBGNIy']"))
    rest_cuisine=driver.find_elements_by_xpath("//*[@class='sc-hdPSEv kBGNIy']")
    
    cuisine_list= []
    for cuisine in rest_cuisine:
        cuisine_list.append(cuisine.text)
    
    # Storing restaurant rating
    WebDriverWait(driver, 100).until(lambda driver: driver.find_element_by_xpath("//*[@class='sc-cgHJcJ jzevHZ']"))
    rest_rating=driver.find_element_by_xpath("//*[@class='sc-cgHJcJ jzevHZ']").text[0]
    
    # Storing restaurant location
    WebDriverWait(driver, 100).until(lambda driver: driver.find_element_by_xpath("//*[@class='sc-cmIlrE kbEObq']"))
    rest_location=driver.find_element_by_xpath("//*[@class='sc-cmIlrE kbEObq']").text
    
    # Storing the data in dataframe
    df = df.append({'Name': rest_name,'cuisine': cuisine_list,'location':rest_location, 'rating':rest_rating,'url':url}, ignore_index=True)   

    driver.close()
    
    # Switching to main window
    driver.switch_to.window(current_window)
    
  
# Storing the dataframe in a CSV file          
df.to_csv("Zomato_data.csv")

