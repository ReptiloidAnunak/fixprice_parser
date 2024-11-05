from pydantic_settings import BaseSettings


from selenium import webdriver
from selenium.webdriver.ie.webdriver import WebDriver


# PROXY = "11.456.448.110:8080"
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--proxy-server=%s' % PROXY)
# chrome = webdriver.Chrome(chrome_options=chrome_options)
# chrome.get("https://www.google.com")


# def set_proxy_chrome_driver(driver: WebDriver, env: BaseSettings):
#
#     print('RUN PROXY SELENIUM DRIVER')
#
#     chome_options = webdriver.ChromeOptions()
#
#     chome_options.add_argument(proxy.make_browser_proxy_server_arg())
#
#     # if user_agent:
#     #     chome_options.add_argument()
#
#     driver = webdriver.Chrome(options=chome_options)
#     driver.get(SITE_CHECK_IP_SELENIUM_BROWSER)
#     # return driver


            # print(proxy)
            # driver = get_chrome_driver(proxy,
            #                   use_proxy=True)
            # driver.get(SITE_CHECK_IP_SELENIUM_BROWSER)
            # time.sleep(15)
            # driver.quit()