import time
from time import sleep

from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, \
    ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.ie.webdriver import WebDriver





def kill_popup_window(driver: WebDriver) -> None:
    try:
        close_popup_window_btn = driver.find_element(By.XPATH, '//*[@id="modal"]/div[1]')
        close_popup_window_btn.click()
        time.sleep(5)
        print('POPUP WINDOW KILLED')
    except (NoSuchElementException, ElementNotInteractableException):
        try:
            close_popup_window_btn = driver.find_element(By.CSS_SELECTOR, '#app-header > header > div > div > div.top-wrapper.shown-overflow > div.left > div.city-obtain.spread > div.choice-city')
            close_popup_window_btn.click()
            time.sleep(5)

        except (NoSuchElementException, ElementNotInteractableException):
            print("No POPUP WINDOW")
            pass

def select_city(driver: WebDriver, city: str = 'Екатеринбург') -> None:
    try:
        no_moscow_btn = driver.find_element(By.XPATH, '//*[@id="app-header"]/header/div/div/div[1]/div[1]/div[1]/div[1]/div/div[2]/button[2]')
        no_moscow_btn.click()
    except NoSuchElementException:
        sleep(3)
        input_city_field = driver.find_element(By.XPATH, '//*[@id="modal"]/div/div[4]/form/input')
        input_city_field.click()
        sleep(1)
        input_city_field.send_keys(city)
        sleep(4)
        found_city = driver.find_element(By.CSS_SELECTOR, '#modal > div > div.search-form > div > div.city')
        found_city.click()
        time.sleep(2)
        submit_city_btn = driver.find_element(By.XPATH, '//*[@id="modal"]/div/div/div/button[2]')
        submit_city_btn.click()
        print(f'City selected: {city}')

    except ElementClickInterceptedException:
        sleep(3)
        sleep(3)
        input_city_field = driver.find_element(By.XPATH, '//*[@id="modal"]/div/div[4]/form/input')
        input_city_field.click()
        sleep(1)
        input_city_field.send_keys(city)
        sleep(4)
        found_city = driver.find_element(By.CSS_SELECTOR, '#modal > div > div.search-form > div > div.city')
        found_city.click()
        time.sleep(2)
        submit_city_btn = driver.find_element(By.XPATH, '//*[@id="modal"]/div/div/div/button[2]')
        submit_city_btn.click()
        print(f'City selected: {city}')


