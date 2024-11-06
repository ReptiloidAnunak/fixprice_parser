import time
from datetime import datetime
from tarfile import data_filter
from time import sleep

from scrapy.http import Response
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.ie.webdriver import WebDriver
from logger.log import create_logger

log = create_logger('Spider fix_price')

def get_brand(response: Response) -> str:
    log.info(get_brand.__name__)
    brand = response.css(
        'html body div#__nuxt div#__layout div.default-layout div.common div.page-content div.centered-layout div.nuxt-content div.container div.content div.product div.product-details div.properties-block div.additional-information div.properties p.property span.value a.link::text').get()
    if not brand:
        brand = "?"
    return brand


def get_images(response: Response) -> dict:
    log.info(get_images.__name__)
    images_lst = response.css('.gallery div div div div img::attr(src)').getall()

    if not images_lst:
        images_lst = response.css(
            'html body div#__nuxt div#__layout div.default-layout div.common div.page-content div.centered-layout div.nuxt-content div.container div.content div.product div.product-images div.slider.gallery div.zoom-on-hover link::attr(href)').getall()

    main_image = images_lst[0]
    assets = dict(main_image=main_image,
                  set_images=images_lst, view360=[], video=[])
    return assets


def get_marketing_tag(response: Response, driver: WebDriver) -> list:
    log.info(get_marketing_tag.__name__)
    driver.get(response.url)
    time.sleep(3)
    tags = []
    try:
        marketing_tag = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div/div[3]/div/div/div/div/div[2]/div[2]/div[1]/div/div/div[1]/div[1]/div[2]').text
        tags.append(marketing_tag)
    except (NoSuchElementException, AttributeError):
        pass

    return tags


def get_price_data(response: Response, driver: WebDriver) -> dict:
    log.info(get_price_data.__name__)
    driver.get(response.url)
    time.sleep(3)
    current_price_str = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div/div[3]/div/div/div/div/div[2]/div[2]/div[1]/div/div/div[1]/div[1]/div[1]/div[1]').text
    current_price = float(current_price_str.split(" ")[0].replace(',', '.'))

    regular_price = float(response.css('div.price-wrapper meta::attr(content)').getall()[1].replace(',', '.'))

    if not current_price:
        current_price = regular_price

    if current_price < regular_price:
        discount = round((regular_price - current_price) / (regular_price / 100))
        sale_tag = f"Скидка {discount}%"
    else:
        sale_tag = '-'
    price_data = dict(current=current_price, original=regular_price, sale_tag=sale_tag)
    return price_data


def get_product_metadata(response: Response) -> dict:
    log.info(get_product_metadata.__name__)
    product_metadata_dict = dict()

    description = response.css('div.description:nth-child(8)::text').get()
    product_metadata_dict["__description"] = description

    properties_rows = response.css('.properties p')
    for st in properties_rows[1:]:
        title = st.css('span.title::text').get()
        value = st.css('span.value::text').get()
        product_metadata_dict[title] = value

    return product_metadata_dict

def get_section(response: Response) -> list:
    log.info(get_section.__name__)
    section = response.css('.breadcrumbs div.crumb div a span::text').getall()
    return section

def get_stock(response: Response, driver: WebDriver) -> dict:
    log.info(get_stock.__name__)
    driver.get(response.url)
    try:
        log.info("Попытка найти элемент get_stock1")
        product_availability_btn = driver.find_element(By.CSS_SELECTOR, '#__layout > div > div > div.page-content > div > div > div > div > div.product > div.product-details > div.controls > div.check-availability > div')
    except NoSuchElementException:
        try:
            log.info("Попытка найти элемент get_stock2")
            sleep(2)
            product_availability_btn = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div/div[3]/div/div/div/div/div[2]/div[2]/div[2]/div[2]/div')
        except NoSuchElementException:
            try:
                log.info("Попытка найти элемент get_stock3")
                sleep(2)
                product_availability_btn = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div/div[3]/div/div/div/div/div[2]/div[2]/div[2]/div[2]/div/svg/path[1]')
            except NoSuchElementException:
                product_availability_btn = driver.find_element(By.CSS_SELECTOR, '#__layout > div > div > div.page-content > div > div > div > div > div.product > div.product-details > div.controls > div.check-availability > div > svg > path:nth-child(1)')
    #

    product_availability_btn.click()
    sleep(5)
    stock_dict = {
        "stock": {"in_stock": True}
    }
    return stock_dict

def get_pages_links(driver: WebDriver, cat_pages_to_scrap) -> list:
    log.info(get_pages_links.__name__)
    try:
        sleep(3)
        pages_div = driver.find_element(By.XPATH,
                                        '//*[@id="__layout"]/div/div/div[3]/div/div/div/div[2]/main/div[2]/div[1]/div[3]/div')
    except NoSuchElementException:
        sleep(3)
        pages_div = driver.find_element(By.CSS_SELECTOR,
                                        '#__layout > div > div > div.page-content > div > div > div > div.catalog > main > div.category-content > div:nth-child(1) > div.controls > div').get()

    pages_btn = pages_div.find_element(By.TAG_NAME, 'a')
    first_page_link = pages_btn.get_attribute('href')

    links = ["=".join([first_page_link.split("=")[0], str(i)]) for i in range(1, cat_pages_to_scrap + 1)]
    return links


def set_timestamp() -> int:
    log.info(set_timestamp.__name__)
    current_time = datetime.now()
    return int(round(current_time.timestamp()))
