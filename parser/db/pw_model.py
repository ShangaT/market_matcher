from peewee import Model, TextField, FloatField, CharField, ForeignKeyField


class Store(Model):
    name = CharField()
    code = CharField()

class Region(Model):
    name = CharField()
class Product(Model):
    product_id = TextField(unique=True)
    store_id = ForeignKeyField(Store, backref='products')
    region_id = ForeignKeyField(Region)
    name = TextField()
    code = TextField()
    category = CharField()
    category_code = CharField()
    price = FloatField()


