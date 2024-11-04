from datetime import datetime

from scrapy.http import Response

def get_brand(response: Response) -> str:
    brand = response.css(
        'html body div#__nuxt div#__layout div.default-layout div.common div.page-content div.centered-layout div.nuxt-content div.container div.content div.product div.product-details div.properties-block div.additional-information div.properties p.property span.value a.link::text').get()
    if not brand:
        brand = "?"
    return brand


def get_images(response: Response) -> dict:
    images_lst = response.css('.gallery div div div div img::attr(src)').getall()

    if not images_lst:
        images_lst = response.css(
            'html body div#__nuxt div#__layout div.default-layout div.common div.page-content div.centered-layout div.nuxt-content div.container div.content div.product div.product-images div.slider.gallery div.zoom-on-hover link::attr(href)').getall()

    main_image = images_lst[0]
    assets = dict(main_image=main_image,
                  set_images=images_lst, view360=[], video=[])
    return assets


def get_special_price_marketing_tag(response: Response):
    special_price_tag = response.css('div.price-wrapper.price div.visible-part div.auth-block p.special-auth::text').get()
    if type(special_price_tag) is str and 'Спец цена' in special_price_tag:
        return ['Спец цена']
    else:
        return [None]



def get_current_price(response: Response):
    response.url

def get_price_data(response: Response) -> dict:
    regular_price = float(response.css('div.price-wrapper meta::attr(content)').getall()[1])
    current_price = response.xpath('/html/body/div[1]/div/div/div/div[3]/div/div/div/div/div[2]/div[2]/div[1]/div/div/div[1]/div[1]/div[1]').get()
    # print('current_price: ', current_price)

    if not current_price:
        current_price = regular_price

    price_data = dict(current=current_price, original=regular_price, sale_tag="?")
    return price_data


def get_product_metadata(response: Response) -> dict:
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
    section = response.css('.breadcrumbs div.crumb div a span::text').getall()
    return section

def set_timestamp() -> int:
    current_time = datetime.now()
    return int(round(current_time.timestamp()))