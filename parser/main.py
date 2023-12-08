
from config import Config
from db.database import Db, createDriver
from db.model import Product
from store.ashan import AshanParser
from store.perekrestok import PerekrestokParser
from store.magnit import MagnitParser

from peewee import chunked

from store.stocks_info import StocksInfo

if __name__ == '__main__':

    # Конфиг парсера
    cfg = Config()
    cfg.read_from_env()

    # драйвер бд
    driver = createDriver(cfg.dbconfig)

    # инстанс бд
    db = Db(driver)
    db.connect()

    # получаем информацию о магазинах
    ashan_stocks = StocksInfo(AshanParser.store_code)
    magnit_stocks = StocksInfo(MagnitParser.store_code)
    perekrestok_stocks = StocksInfo(PerekrestokParser.store_code)

    # парсим продукты 
    # TODO сделать по stockId
    ashan_products = AshanParser(stockId=1).start()
    magnit_products = MagnitParser(stockId=773797).start()
    perekrestok_products = PerekrestokParser(stockId=400).start()

    # записываем продукты в бд
    with db.pool.atomic():
        for batch in chunked([p.__data__ for p in [*magnit_products]], 100):
            Product.insert_many(batch).on_conflict_ignore().execute()
