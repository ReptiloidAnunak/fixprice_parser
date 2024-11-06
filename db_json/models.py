import json

from pydantic import BaseModel
from typing import List, Optional, Union

from config import DB_JSON
from fixprice.spiders.spider_tools import set_timestamp


class Category(BaseModel):
    name: str
    link: str

    def to_dict(self):
        return {self.name: self.link, "products": []}

    def is_in_result_json(self):
        try:
            with open(DB_JSON, 'r') as file:
                content = json.load(file)
                cat_names_pairs_json = [list(d.keys()) for d in content]
                cat_names_json = [pair[0] for pair in cat_names_pairs_json]
                print("cat_names_json: ", cat_names_json)
                if self.name in cat_names_json:
                    print(f'{self.name} is already in JSON')
                    return True
                else:
                    return False
        except FileNotFoundError:
            with open(DB_JSON, "w") as file:
                json.dump([], file, indent=4)


class Product(BaseModel):
    category: dict
    timestamp: int
    title: str
    rpc: Optional[str]
    url: str
    marketing_tags: Optional[List[Union[str, None]]]
    brand: str
    section: Optional[List[str]]
    price_data: Optional[dict]
    stock: Optional[dict] = {}
    assets: Optional[dict]
    metadata: Optional[dict]
    variants: Optional[int] = 1


    def __init__(self, category: dict, title: str, url: str, brand: str,
                 rpc: Optional[str],
                 section: Optional[List[str]], price_data: Optional[dict],assets: Optional[dict],
                 metadata: Optional[dict],
                 stock: Optional[dict] = None,
                 marketing_tags: Optional[List[str]] = None,
                 variants: Optional[int] = None):
        super().__init__(
            category=category,
            timestamp=set_timestamp(),
            title=title,
            rpc=rpc,
            url=url,
            marketing_tags=marketing_tags,
            brand=brand,
            section=section,
            price_data=price_data,
            stock=stock,
            assets=assets,
            metadata=metadata,
            variants=variants
        )


    def create_result_dict(self):
        return {
    "timestamp": self.timestamp,  # Дата и время сбора товара в формате timestamp.
    "RPC": self.rpc,  # Уникальный код товара.
    "url": self.url,  # Ссылка на страницу товара.
    "title": self.title,  # Заголовок/название товара (! Если в карточке товара указан цвет или объем, но их нет в названии, необходимо добавить их в title в формате: "{Название}, {Цвет или Объем}").
    "marketing_tags": self.marketing_tags,  # Список маркетинговых тэгов, например: ['Популярный', 'Акция', 'Подарок']. Если тэг представлен в виде изображения собирать его не нужно.
    "brand": self.brand,  # Бренд товара.
    "section": self.section,  # Иерархия разделов, например: ['Игрушки', 'Развивающие и интерактивные игрушки', 'Интерактивные игрушки'].
    "price_data": self.price_data,
    "stock": self.stock,
    "assets": self.assets,
    "metadata": self.metadata,
    "variants": self.variants,  # Кол-во вариантов у товара в карточке (За вариант считать только цвет или объем/масса. Размер у одежды или обуви варинтами не считаются).
}

    # def is_in_result_json(self):

    def is_in_json_result(self):
        print(f"product {self.title} -- save_to_result_json")
        with open(DB_JSON, "rs") as file:
            content = json.load(file)


    def save_to_result_json(self):
        print(f"product {self.title} -- save_to_result_json")
        with open(DB_JSON, "r+") as file:
            content = json.load(file)
            rel_cat = [d for d in content if list(self.category.keys())[0] in list(d.keys())][0]
            new_product = self.create_result_dict()
            if new_product not in rel_cat['products']:
                rel_cat['products'].append(new_product)
            else:
                print("ALREADY in JSON: ", self.title, self.rpc)
            file.seek(0)
            json.dump(content, file, indent=4)

    def __str__(self):
        return self.title
