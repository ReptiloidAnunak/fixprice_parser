import os.path

from pydantic_settings import BaseSettings


from selenium import webdriver
from selenium.webdriver.ie.webdriver import WebDriver
from config import env, Config, ROOT_DIR, START_URL
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
print(env.PROXY_PORT)


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

def set_proxy_chrome_driver() -> webdriver.Chrome:

    chrome_options = Options()
    proxy = f'{env.PROXY_USER}:{env.PROXY_PASS}@{env.PROXY_IP}:{env.PROXY_PORT}'
    chrome_proxy_arg = f'--proxy-server=http://{proxy}'
    chrome_options.add_argument(chrome_proxy_arg)

    chromedriver_path = os.path.join(ROOT_DIR, 'chromedriver')  # Замените на свой путь к chromedriver

    driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
    driver.maximize_window()

    driver.get(START_URL)

    window_handles = driver.window_handles

    if len(window_handles) > 1:
        driver.switch_to.window(window_handles[1])
        driver.close()

    driver.switch_to.window(window_handles[0])
    return driver
