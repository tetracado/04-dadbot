from selenium import webdriver
import platform
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import re
import os

import pickle

mydir=os.path.dirname(__file__)


options=Options()
#options.BinaryLocation='/usr/bin/chromium-browser'
options.add_argument('--disable-infobars')
options.add_argument('--disable-extensions')
options.add_argument('--disable-gpu')
#options.add_argument('--headless')
#options.add_argument('--window-size=1024,1068')
driver_path='/usr/bin/chromedriver'

service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(options=options,service=service)


def openlink(link):
    print('opening:',link)
    driver.get(link)
    time.sleep(5)

def getdetails():
    #date=driver.find_element(By.CLASS_NAME, "mdl-card__title-text")
    #date=date.text
    #date=re.sub("Holiday.+day, ", "", date)
    titles=driver.find_elements(By.CLASS_NAME, "mdl-card__title-text")
    #date=re.sub("Holiday.+day, ", "", titles[0].text)
    holidays=[]
    for element in titles:
        text=element.text
        if "Holidays for" in text:
            date=re.sub("Holiday.+day, ", "", text)
            continue
        if "On This Day in History" in text:
            return (date,holidays)
        else:
            holidays.append(text)
        #print(element.text)
    #print(date)

def stealholidays():
    holidays={}
    openlink(testlink)
    days=0
    while days < 370:
        today=getdetails()
        holidays[today[0]]=today[1]
        days+=1
        links=driver.find_elements(By.TAG_NAME, "a")
        tomorrow=links[14].get_attribute("href")
        #for element in links:
            #print(element.get_attribute("href"))

        #print(tomorrow)
        openlink(tomorrow)
    with open('holidays.pkl', 'wb') as f:
        pickle.dump(holidays, f)

testlink='https://www.checkiday.com/1/1/2023'
stealholidays()
#print(getdetails())