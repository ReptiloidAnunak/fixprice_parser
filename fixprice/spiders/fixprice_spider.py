import subprocess

import scrapy
from scrapy.http import Response
from twisted.conch.ssh.sexpy import parse

from config import Nodes
from models import Category


proxy_user = 'n3ZDjKaZ'
proxy_pass = 'nKwaNGmT'
proxy_ip = '212.193.190.236'
proxy_port = '62894'


class FixPriceSpider(scrapy.Spider):
    name = 'fix_price'
    start_urls = ["https://fix-price.com/"]
    selected_categories = []

    def start_requests(self) -> None:
        yield scrapy.Request(self.start_urls[0],
                             meta={'proxy': f'http://{proxy_user}:{proxy_pass}@{proxy_ip}:{proxy_port}'})

    def parse(self, response: Response) -> None:
            self.parse_categories_lst(response)

    def parse_categories_lst(self, response: Response) -> None:
        categories_divs = response.css("body div.categories a")
        categories_lst = []
        for cat_div in categories_divs:
            category = Category(name=cat_div.css("::text").get(),
                                link="/".join([self.start_urls[0], cat_div.attrib["href"]]))
            categories_lst.append(category)

        self.selected_categories.append(categories_lst[-2])  # Example
        print("Выбранные категории:", self.selected_categories)

        yield response.follow_all(self.selected_categories, self.parse_goods)
    #
    #
    def parse_goods(self, response: Response):
        products_div = response.xpath('/html/body/div[1]/div/div/div/div[3]/div/div/div/div[2]/main/div[2]/div[1]/div[2]').get()
        print(products_div)




if __name__ == "__main__":
    subprocess.run(['scrapy', 'crawl', FixPriceSpider.name])