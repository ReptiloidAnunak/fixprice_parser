import scrapy
from scrapy.http import Response
from config import env
from fixprice.models import Category, Product

import logging

from fixprice.spiders.spider_tools import get_images, get_brand, get_price_data, get_product_metadata, \
    get_marketing_tags

log = logging.Logger(name='fix-price')
log.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
log.addHandler(console_handler)


class FixPriceSpider(scrapy.Spider):
    name = 'fix_price'
    start_urls = ["https://fix-price.com/"]


    def start_requests(self) -> None:
        yield scrapy.Request(self.start_urls[0],
                             meta={'proxy': f'http://{env.PROXY_USER}:{env.PROXY_PASS}@{env.PROXY_IP}:{env.PROXY_PORT}'})

    def parse(self, response: Response) -> None:

        categories_divs = response.css("body div.categories a")
        categories_lst = []
        selected_categories = []

        for cat_div in categories_divs:
            category = Category(name=cat_div.css("::text").get(),
                                link="/".join([self.start_urls[0], cat_div.attrib["href"]]))
            categories_lst.append(category)

        selected_categories.append(categories_lst[-2])  # Example
        log.info(f"Выбранные категории: {str(selected_categories)}")

        selected_cat_list = [cat for cat in selected_categories]
        for cat in selected_cat_list:
            yield response.follow(cat.link, self.parse_product, cb_kwargs={"category": cat})

    def parse_product(self, response: Response, category: Category):
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
                          marketing_tags=get_marketing_tags(response)
                          )

        category.products_lst.append(product)

        print(response.url)
        print(product)
        print('_________________')


# Может отсюда получится вытянуть специальную цену
# <div class="product__wrapper" data-v-30abd08e><div id="cp3130179" class="product one-product-in-row" data-v-7d139f34 data-v-30abd08e><div class="wrapper sticker" data-v-4dbc8b28 data-v-7d139f34><!----><!----></div><div class="images-container" data-v-7d139f34><!----></div><div class="details" data-v-7d139f34><div class="information" data-v-7d139f34><div class="description" data-v-7d139f34><a href="/catalog/kosmetika-i-gigiena/p-3130179-tualetnaya-bumaga-omfort-amilia-2-sloya-32-rulona" class="title" data-v-7d139f34>Туалетная бумага "Comfort", Familia, 2 слоя, 32 рулона</a><!----><div itemprop="offers" itemscope="itemscope" itemtype="http://schema.org/Offer" class="price-wrapper price-block" data-v-06f8b9a7 data-v-7d139f34><!----><div class="visible-part card" data-v-06f8b9a7><!----><!----></div></div></div><button data-test="button" data-metrics="not-send" width="21" height="21" class="favorites button-favorites without-text" data-v-84e4fc10 data-v-7d139f34><img width="21" height="21" stroke="#0A54CC" src="/img/common/bookmark.svg" class="icon" data-v-84e4fc10><!----></button></div><!----></div></div></div>

if __name__ == "__main__":
    from scrapy.cmdline import execute
    execute(['scrapy', 'crawl', FixPriceSpider.name])