import os.path
import subprocess
from scrapy.cmdline import execute
import scrapy
from scrapy.http import Response
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.ie.webdriver import WebDriver

from db_json.db_tools import get_product_by_cat_rpc
from fixprice.driver.service import select_city_serv
from db_json.models import Category, Product
from fixprice.spiders.spider_tools import get_images, get_brand, get_price_data, get_product_metadata, \
    get_marketing_tag, get_section, get_pages_links
from fixprice.tools import save_to_result_json_lst
from logger.log import create_logger

log = create_logger('Spider fix_price')

class FixPriceSpider(scrapy.Spider):
    name = 'fix_price'
    start_urls = ["https://fix-price.com/"]

    def start_requests(self) -> None:
        url = "https://fix-price.com/"
        yield SeleniumRequest(url=url, callback=self.parse, wait_time=100)

    def parse(self, response: Response) -> None:
        driver = response.request.meta["driver"]
        select_city_serv(driver, self.start_urls[0])

        categories_divs = response.css("body div.categories a")
        categories_lst = []
        selected_categories = []

        for cat_div in categories_divs:
            category = Category(name=cat_div.css("::text").get(),
                                link="/".join([self.start_urls[0], cat_div.attrib["href"]]))
            categories_lst.append(category)

        for cat in categories_lst:
            log.info(f"cat.name: {cat.name}")
            if not cat.is_in_result_json():
                save_to_result_json_lst(cat.to_dict())

        selected_categories.extend([categories_lst[1], categories_lst[-2]])  # Example
        selected_cat_list = [cat for cat in selected_categories]
        for cat in selected_cat_list:
            yield response.follow(cat.link, self.parse_cat_pages_lst, cb_kwargs={"category": cat, "driver": driver})

    def parse_cat_pages_lst(self, response: Response, driver, category: Category):
       log.info(self.parse_cat_pages_lst.__name__)
       cat_pages_to_scrap = 3
       driver.get(response.url)
       pages_links = get_pages_links(driver, cat_pages_to_scrap)

       for p_link in pages_links:
           log.info(f"Current_page_url: {p_link}")
           yield response.follow(p_link, self.parse_cat_page, cb_kwargs={"driver": driver, "category": category})

    def parse_cat_page(self, response: Response, driver, category: Category):
        log.info(self.parse_cat_page.__name__)
        products_wrappers = response.css('div.product__wrapper')
        for wrapper in products_wrappers:
            product_link = wrapper.css('a').attrib["href"]
            rpc = wrapper.css('div div').attrib['id']
            if not get_product_by_cat_rpc(category.name, rpc):
                yield response.follow(product_link, self.parse_product_page, cb_kwargs={"driver": driver, 'rpc': rpc, "category": category})
            else:
                log.info(f'ALREADY IN DB: product rpc:: {rpc} category:: {category.name}')
                return

    def parse_product_page(self, response: Response, driver: WebDriver, rpc: str, category: Category):
        log.info(f'Current product`s page: {response.url}')
        product = Product(category=category.to_dict(),
                          rpc=rpc,
                          title=response.css('h1.title::text').get(),
                          brand=get_brand(response),
                          url=response.url,
                          assets=get_images(response),
                          price_data=get_price_data(response, driver),
                          metadata=get_product_metadata(response),
                          marketing_tags=get_marketing_tag(response, driver),
                          section=get_section(response)
                          # stock=get_stock(response, driver) #Problematic element
                          )

        product.save_to_result_json()
        print('_________________')


if __name__ == "__main__":
    subprocess.run(["python", str(os.path.join("interface", "result_flask.py"))])
    execute(['scrapy', 'crawl', FixPriceSpider.name])