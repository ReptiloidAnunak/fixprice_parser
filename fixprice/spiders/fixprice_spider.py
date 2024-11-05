
import scrapy
from scrapy.http import Response
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.ie.webdriver import WebDriver

from fixprice.driver.service import select_city_serv
from fixprice.models import Category, Product
from fixprice.spiders.spider_tools import get_images, get_brand, get_price_data, get_product_metadata, \
    get_marketing_tag, get_section
from tools import save_to_result_json_lst


class FixPriceSpider(scrapy.Spider):
    name = 'fix_price'
    start_urls = ["https://fix-price.com/"]


    def start_requests(self) -> None:
        url = "https://fix-price.com/"
        yield SeleniumRequest(url=url, callback=self.parse, wait_time=100)

    def parse(self, response: Response) -> None:

        driver = response.request.meta["driver"]
        select_city_serv(response, driver, self.start_urls[0])

        categories_divs = response.css("body div.categories a")
        categories_lst = []
        selected_categories = []

        for cat_div in categories_divs:
            category = Category(name=cat_div.css("::text").get(),
                                link="/".join([self.start_urls[0], cat_div.attrib["href"]]))
            categories_lst.append(category)

        for cat in categories_lst:
            print("cat.name: ", cat.name)
            if not cat.is_in_result_json():
                save_to_result_json_lst(cat.to_dict())

        selected_categories.extend([categories_lst[1], categories_lst[-2]])  # Example

        selected_cat_list = [cat for cat in selected_categories]
        for cat in selected_cat_list:

            yield response.follow(cat.link, self.parse_cat_page, cb_kwargs={"category": cat, "driver": driver})

    def parse_cat_page(self, response: Response, driver, category: Category):
        products_wrappers = response.css('div.product__wrapper')

        for wrapper in products_wrappers:
            product_link = wrapper.css('a').attrib["href"]
            rpc = wrapper.css('div div').attrib['id']

            yield response.follow(product_link, self.parse_product_page, cb_kwargs={"driver": driver, 'rpc': rpc, "category": category})

    def parse_product_page(self, response: Response, driver: WebDriver, rpc: str, category: Category):
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
                          )

        #
        print(response.url)
        product.save_to_result_json()
        print('_________________')




if __name__ == "__main__":
    from scrapy.cmdline import execute
    execute(['scrapy', 'crawl', FixPriceSpider.name])