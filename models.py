from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

class Category(BaseModel):
    name: str
    link: str


class Product(BaseModel):
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


    def __init__(self, title: str, url: str, brand: str,
                 rpc: Optional[str] = None, marketing_tags: Optional[List[str]] = None,
                 section: Optional[List[str]] = None, price_data: Optional[dict] = None,
                 stock: Optional[dict] = None, assets: Optional[dict] = None,
                 metadata: Optional[dict] = None, variants: Optional[int] = None):
        super().__init__(
            timestamp=self._set_timestamp(),
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

    def _set_timestamp(self) -> int:
        current_time = datetime.now()
        return int(round(current_time.timestamp()))




# {
#     "timestamp": int,  # Дата и время сбора товара в формате timestamp.
#     "RPC": "str",  # Уникальный код товара.
#     "url": "str",  # Ссылка на страницу товара.
#     "title": "str",  # Заголовок/название товара (! Если в карточке товара указан цвет или объем, но их нет в названии, необходимо добавить их в title в формате: "{Название}, {Цвет или Объем}").
#     "marketing_tags": ["str"],  # Список маркетинговых тэгов, например: ['Популярный', 'Акция', 'Подарок']. Если тэг представлен в виде изображения собирать его не нужно.
#     "brand": "str",  # Бренд товара.
#     "section": ["str"],  # Иерархия разделов, например: ['Игрушки', 'Развивающие и интерактивные игрушки', 'Интерактивные игрушки'].
#     "price_data": {
#         "current": float,  # Цена со скидкой, если скидки нет то = original.
#         "original": float,  # Оригинальная цена.
#         "sale_tag": "str"  # Если есть скидка на товар то необходимо вычислить процент скидки и записать формате: "Скидка {discount_percentage}%".
#     },
#     "stock": {
#         "in_stock": bool,  # Есть товар в наличии в магазине или нет.
#         "count": int  # Если есть возможность получить информацию о количестве оставшегося товара в наличии, иначе 0.
#     },
#     "assets": {
#         "main_image": "str",  # Ссылка на основное изображение товара.
#         "set_images": ["str"],  # Список ссылок на все изображения товара.
#         "view360": ["str"],  # Список ссылок на изображения в формате 360.
#         "video": ["str"]  # Список ссылок на видео/видеообложки товара.
#     },
#     "metadata": {
#         "__description": "str",  # Описание товара
#         "KEY": "str",
#         "KEY": "str",
#         "KEY": "str"
#         # Также в metadata необходимо добавить все характеристики товара которые могут быть на странице.
#         # Например: Артикул, Код товара, Цвет, Объем, Страна производитель и т.д.
#         # Где KEY - наименование характеристики.
#     }
#     "variants": int,  # Кол-во вариантов у товара в карточке (За вариант считать только цвет или объем/масса. Размер у одежды или обуви варинтами не считаются).
# }