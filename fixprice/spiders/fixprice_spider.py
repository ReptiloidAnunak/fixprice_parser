import time

import scrapy
from scrapy.http import Response
from scrapy_selenium import SeleniumRequest

from fixprice.driver.service import select_city_serv
from fixprice.models import Category, Product
from fixprice.spiders.spider_tools import get_images, get_brand, get_price_data, get_product_metadata, \
    get_special_price_marketing_tag, get_section

class FixPriceSpider(scrapy.Spider):
    name = 'fix_price'
    start_urls = ["https://fix-price.com/"]


    def start_requests(self) -> None:
        url = "https://fix-price.com/"
        yield SeleniumRequest(url=url, callback=self.parse, wait_time=100)

    def parse(self, response: Response) -> None:
        select_city_serv(response, self.start_urls[0])
        categories_divs = response.css("body div.categories a")
        categories_lst = []
        selected_categories = []

        for cat_div in categories_divs:
            category = Category(name=cat_div.css("::text").get(),
                                link="/".join([self.start_urls[0], cat_div.attrib["href"]]))
            categories_lst.append(category)

        selected_categories.extend([categories_lst[1], categories_lst[-2]])  # Example

        selected_cat_list = [cat for cat in selected_categories]
        for cat in selected_cat_list:

            yield response.follow(cat.link, self.parse_cat_page, cb_kwargs={"category": cat})

    def parse_cat_page(self, response: Response, category: Category):
        products_wrappers = response.css('div.product__wrapper')

        for wrapper in products_wrappers:
            product_link = wrapper.css('a').attrib["href"]
            rpc = wrapper.css('div div').attrib['id']

            yield response.follow(product_link, self.parse_product_page, cb_kwargs={'rpc': rpc, "category": category})


    def parse_product_page(self, response: Response, rpc: str, category: Category):
        product = Product(category=category.to_dict(),
                          rpc=rpc,
                          title=response.css('h1.title::text').get(),
                          brand=get_brand(response),
                          url=response.url,
                          assets=get_images(response),
                          price_data=get_price_data(response),
                          metadata=get_product_metadata(response),
                          marketing_tags=get_special_price_marketing_tag(response),
                          section=get_section(response)
                          )

        category.products_lst.append(product)

        print(response.url)
        print(product)
        print('_________________')


    def get_current_price(self, response: Response):
        current_price = response.xpath('/html/body/div[1]/div/div/div/div[3]/div/div/div/div/div[2]/div[2]/div[1]/div/div/div[1]/div[1]/div[1]/div[1]')
        if current_price:
            print('CURRENT PRICE: ', current_price.get())
        else:
            print('Цена не найдена.')


if __name__ == "__main__":
    from scrapy.cmdline import execute
    execute(['scrapy', 'crawl', FixPriceSpider.name])