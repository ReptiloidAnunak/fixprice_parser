import json

from config import DB_JSON


def get_product_by_cat_rpc(cat_name: str, rpc: str):
    with open(DB_JSON, 'r') as file:
        content_json = json.loads(file.read())
        db_rel_cat = [d for d in content_json if list(d.keys())[0] == cat_name][0]
        all_cat_products = db_rel_cat['products']
        # print("all_cat_products: ", all_cat_products)
        prod_from_db = [product for product in all_cat_products if len(product['RPC']) > 0 and product['RPC'] == rpc]
        if len(prod_from_db) == 0:
            return False
        return prod_from_db