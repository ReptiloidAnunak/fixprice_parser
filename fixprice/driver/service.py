from selenium.webdriver.ie.webdriver import WebDriver
from fixprice.driver.functions import kill_popup_window, select_city
from scrapy.http import Response
import time


def select_city_serv(response: Response, driver, start_url):
    driver.set_window_size(1044, 768)
    driver.get(start_url)
    time.sleep(3)
    kill_popup_window(driver)
    time.sleep(4)
    select_city(driver)