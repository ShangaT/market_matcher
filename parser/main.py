
from multiprocessing.pool import ThreadPool
import sys
from config import Config
from db.database import Db, createDriver
# from db.model import Product
from db.pw_model import Product
from store.ashan import AshanParser
from store.perekrestok import PerekrestokParser
from store.magnit import MagnitParser
from pypika import Table, Query

from more_itertools import chunked

from store.stocks_info import StocksInfo

if __name__ == '__main__':

    # Конфиг парсера
    cfg = Config()
    cfg.read_from_env()

    print(cfg.dbconfig.__dict__)

    # драйвер бд
    driver = createDriver(cfg.dbconfig)

    # инстанс бд
    db = Db(driver)
    db.connect()

    # ищем аргумент parse
    args = sys.argv[1:]
    must_parse = False
    if len(args) > 0:
        if args[0] == 'parse':
            must_parse = True

    if not must_parse:
        print('Add arg "parse" to start parser')
        exit(1)

    # получаем информацию о магазинах
    ashan_stocks = StocksInfo(AshanParser.store_code)
    magnit_stocks = StocksInfo(MagnitParser.store_code)
    perekrestok_stocks = StocksInfo(PerekrestokParser.store_code)

    # TODO сделать по stockId
    # парсеры
    ap = AshanParser(stockId=ashan_stocks.stocks[2].stockId)
    mp = MagnitParser(stockId=magnit_stocks.stocks[2].stockId)
    pp = PerekrestokParser(stockId=perekrestok_stocks.stocks[2].stockId)


    parsers = [ap, mp, pp]
    products = []

    def parse_callback(parse_result: list):
        products.extend(parse_result)

    # парсим продукты многопоточно
    with ThreadPool(processes=len(parsers)) as pool:
        for parser in parsers:
            pool.apply_async(parser.start, callback=parse_callback)
        pool.close() 
        pool.join()  

    print('Parsed products = ', len(products))

    with db.pool.atomic():
        for batch in chunked([p.__data__ for p in products], 100):
            Product.insert_many(batch).on_conflict_ignore().execute()

    # chunk_size = 100
    # chunks: list[list[Product]] = list(chunked(products, chunk_size))

    # # записываем продукты в бд
    # ptable = Table('product')
    # for chunk in chunks:
    #     q = Query.into(ptable).columns(ptable.product_id, ptable.store_id, ptable.name, ptable.code, ptable.category, ptable.category_code, ptable.price)
        
    #     for item in chunk:
    #         q = q.insert(item.product_id, item.store_id, item.name, item.code, item.category, item.category_code, item.price)

    #     q = q.on_conflict(ptable.product_id).do_nothing()
        
    #     db.pool.execute_sql(str(q))
