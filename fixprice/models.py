from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

from fixprice.spiders.spider_tools import set_timestamp


class Category(BaseModel):
    name: str
    link: str
    products_lst: list = []

    def to_dict(self):
        return {self.name: self.link}


class Product(BaseModel):
    category: dict
    timestamp: int
    title: str
    rpc: Optional[str] = None
    url: str
    marketing_tags: Optional[List[str]] = None
    brand: str
    section: Optional[List[str]] = None
    price_data: Optional[dict] = None
    stock: Optional[dict] = None
    assets: Optional[dict] = None
    metadata: Optional[dict] = None
    variants: Optional[int] = None


    def __init__(self, category: dict, title: str, url: str, brand: str,
                 rpc: Optional[str] = None, marketing_tags: Optional[List[str]] = None,
                 section: Optional[List[str]] = None, price_data: Optional[dict] = None,
                 stock: Optional[dict] = None, assets: Optional[dict] = None,
                 metadata: Optional[dict] = None, variants: Optional[int] = None):
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
    "section": ["str"],  # Иерархия разделов, например: ['Игрушки', 'Развивающие и интерактивные игрушки', 'Интерактивные игрушки'].
    "price_data": self.price_data,
    "stock": {
        "in_stock": bool,  # Есть товар в наличии в магазине или нет.
        "count": int  # Если есть возможность получить информацию о количестве оставшегося товара в наличии, иначе 0.
    },
    "assets": self.assets,
    "metadata": self.metadata,
    "variants": int,  # Кол-во вариантов у товара в карточке (За вариант считать только цвет или объем/масса. Размер у одежды или обуви варинтами не считаются).
}