import os
from peewee import *
from db.config import DBConfig
from db.model import *


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

        self.pool.create_tables([Store, Product])

        self._add_stores()

    def _add_stores(self):
        Store.get_or_create(name='Ашан', code='ashan', id=1)
        Store.get_or_create(name='Магнит', code='magnit', id=2)
        Store.get_or_create(name='Перекресток', code='perekrestok', id=3)
