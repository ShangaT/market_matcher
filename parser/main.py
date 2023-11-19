from db.model import Product
from store.ashan import AshanParser
from store.perekrestok import PerekrestokParser
from store.magnit import MagnitParser

from db import config
from peewee import chunked


if __name__ == '__main__':
    
    db = config.init()

    ashan_products = AshanParser(stockId=1).start()
    magnit_products = MagnitParser(stockId=773797).start()
    perekrestok_products = PerekrestokParser(stockId=400).start()

    with db.atomic():
        for batch in chunked([p.__data__ for p in [*ashan_products, *magnit_products, *perekrestok_products]], 100):
            Product.insert_many(batch).on_conflict_ignore().execute()
