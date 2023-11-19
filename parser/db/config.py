from db.database import db
from db.model import Store, Product

def init():
    db.connect()
    db.create_tables([Store, Product])

    add_stores()

    return db


def add_stores():

    Store.get_or_create(name='Ашан', code='ashan', id=1)
    Store.get_or_create(name='Магнит', code='magnit', id=2)
    Store.get_or_create(name='Перекресток', code='perekrestok', id=3)

    # if not Store.select().count() == 0:
    #     Store.get_or_create(name='Ашан', code='ashan', id=1)
    #     Store.get_or_create(name='Магнит', code='magnit', id=2)
    #     Store.get_or_create(name='Ашан', code='ashan', id=3)
