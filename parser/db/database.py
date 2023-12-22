from more_itertools import chunked
from peewee import PostgresqlDatabase, Database, SqliteDatabase, EXCLUDED
from db.config import DBConfig

from db.pw_model import Product, Store, Region


def create_driver(dbconfig: DBConfig) -> Database:
    match dbconfig.driver.lower():
        case "postgres":
            return PostgresqlDatabase(database=dbconfig.dbname, user=dbconfig.user,
                                      password=dbconfig.pwd, host=dbconfig.host,
                                      port=dbconfig.port)
        case "sqlite":
            return SqliteDatabase(dbconfig.dbname+'.db')


class Db:
    def __init__(self, database: Database) -> None:
        self.pool = database
        self.models = [Store, Region,  Product]

    def connect(self, docker: bool):
        self.pool.connect()

        self.pool.bind(self.models)
        if not docker:
            self.pool.create_tables(self.models)

        self._add_stores()
        self._add_regions()

    def _add_stores(self):
        Store.get_or_create(name='Ашан', code='ashan', id=1)
        Store.get_or_create(name='Магнит', code='magnit', id=2)
        Store.get_or_create(name='Перекресток', code='perekrestok', id=3)

    def _add_regions(self):
        Region.get_or_create(name='Москва', id=77)
        Region.get_or_create(name='Санкт-Петербург', id=78)
        Region.get_or_create(name='Пермь', id=59)

    def add_products(self, products: list[Product], batch_size: int):
        with self.pool.atomic():
            for batch in chunked([p.__data__ for p in products], batch_size):
                (Product
                         .insert_many(batch)
                         .on_conflict(
                             conflict_target=[Product.product_id],
                             preserve=[],
                             update={Product.price: EXCLUDED.price})
                         .execute())
                # Product.insert_many(batch).on_conflict_ignore().execute()
