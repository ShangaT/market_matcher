from peewee import PostgresqlDatabase, Database, SqliteDatabase
from db.config import DBConfig
from pypika import Query

from db.pw_model import Product, Store


def createDriver(dbconfig: DBConfig) -> Database:
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

    def connect(self):
        self.pool.connect()

        self.pool.bind([Store, Product])

        # self.pool.create_tables([Store, Product])

        self._add_stores()

    def _add_stores(self):
        Store.get_or_create(name='Ашан', code='ashan', id=1)
        Store.get_or_create(name='Магнит', code='magnit', id=2)
        Store.get_or_create(name='Перекресток', code='perekrestok', id=3)

    # def connect(self):
    #     self.pool.connect()

    #     self._add_stores()

    # def _add_stores(self):
    #     print(self.pool is PostgresqlDatabase)
    #     q = Query.into('store').columns('id', 'name', 'code').insert(1, 'Ашан', 'ashan').insert(
    #         2, 'Магнит', 'magnit').insert(3, 'Перекресток', 'perekrestok')
    #     self.pool.execute_sql(str(q))
