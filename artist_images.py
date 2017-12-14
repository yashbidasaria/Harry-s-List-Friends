import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome('/Users/evandweck/Desktop/scripts/chromedriver')
x = 0
images_list = []

# find a picture for every artist stepping through the csv one by one...
with open('artist_names.csv') as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for artist in csvReader:
        print(artist)
        print(x)
        driver.get('https://www.google.com/imghp')
        search = driver.find_element_by_name('q')
        search.send_keys(str(artist))
        search.send_keys(Keys.RETURN)
        button = driver.find_elements_by_css_selector("#rg_s > div:nth-child(1) > a > img")
        #image =driver.get_element_by_xpath("//*[@id='rg_s']/div[1]/a/img").click()
        for i in button:
            i.click()
            visit_site = driver.find_elements_by_css_selector("#irc_cc > div:nth-child(2) > div.irc_b.i8152.irc_mmc > div.i30053 > div > table._FKw.irc_but_r > tbody > tr > td:nth-child(2) > a")
            for v in visit_site:
                images_list.append(v.get_attribute('href'))
                break
            x = x+1
            #break

# write each URL to a file
file = open('image_links.csv', 'w')
for i in images_list:
    file.write(i + "\n")
file.close()









