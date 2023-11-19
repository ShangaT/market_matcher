from peewee import Model, TextField, FloatField, CharField, ForeignKeyField
from db.database import db

class BaseModel(Model):
    class Meta:
        database = db


class Store(BaseModel):
    name = CharField()
    code = CharField()

class Product(BaseModel):
    product_id = TextField(unique=True)
    store_id = ForeignKeyField(Store, backref='products')
    name = TextField()
    code = TextField()
    category = CharField()
    category_code = CharField()
    price = FloatField()



