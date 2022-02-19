from datetime import datetime
from time import sleep
from traceback import print_exception
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def exception_info(exception):
    print(type(exception))
    print(exception.args)
    print(exception)

def check_target(driver, urls):
    for key in urls:
        try:
            driver.get(urls[key])
            try:
                elem = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//div[@data-test='orderPickupMessage']")))
                if elem:
                    print("Found " + key + " at " + urls[key])
            except TimeoutException:
                print(key + " at " + urls[key] + " is unavailable")
            except Exception as e:
                exception_info(e)
        except Exception as e:
            exception_info(e)


opts = Options()
opts.headless = True
driver = webdriver.Firefox(options=opts)

target_urls = {'Xbox Series S': 'https://www.target.com/p/xbox-series-s-console/-/A-80790842',
               'Xbox Series X': 'https://www.target.com/p/xbox-series-x-console/-/A-80790841'}

while True:
    check_target(driver, target_urls)