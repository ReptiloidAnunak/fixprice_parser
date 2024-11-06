from selenium.webdriver.ie.webdriver import WebDriver
from fixprice.driver.functions import kill_popup_window, select_city
from scrapy.http import Response
import time
from logger.log import create_logger

log = create_logger('fixprice')

def select_city_serv(driver, start_url):
    log.info(select_city_serv.__name__)
    driver.get(start_url)
    time.sleep(5)
    kill_popup_window(driver)
    time.sleep(4)
    select_city(driver)