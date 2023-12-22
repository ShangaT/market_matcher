from multiprocessing.pool import ThreadPool
import sys
from config import Config
from db.database import Db, create_driver
from store.ashan import AshanParser
from store.perekrestok import PerekrestokParser
from store.magnit import MagnitParser
from store.stocks_info import StocksInfo

BATCH_SIZE = 100

def remove_duplicates(products: list) -> list:
    seen = {}
    for obj in products:
        if obj.product_id not in seen:
            seen[obj.product_id] = obj
    return list(seen.values())


def parse_stores(parsers: list, db: Db):
    for parser in parsers:
        products = remove_duplicates(parser.start())
        db.add_products(products, BATCH_SIZE)
        print(f'{parser.__class__}_{
              parser.stock.region}: parsed products {len(products)}')

def parse():
    # конфиг парсера
    cfg = Config()
    cfg.read_from_env()

    # драйвер базы данных
    driver = create_driver(cfg.dbconfig)

    # инстанс базы данных
    db = Db(driver)
    db.connect(cfg.docker)

    # аргумент parse для запуска парсера
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

    # парсеры
    aps = [AshanParser(stock=s) for s in ashan_stocks.stocks]
    mps = [MagnitParser(stock=s) for s in magnit_stocks.stocks]
    pps = [PerekrestokParser(stock=s) for s in perekrestok_stocks.stocks]

    parse_groups = [
        aps, 
        mps, 
        pps
        ]

    # парсинг продукты многопоточно
    with ThreadPool(processes=len(parse_groups)) as pool:
        for group in parse_groups:
            pool.apply_async(func=parse_stores, args=(group, db))
        pool.close()
        pool.join()


if __name__ == '__main__':
    parse()
