# from django.db import models
# from parser.db.database import db

# class BaseModel(models.Model):
#     class Meta:
#         database = db


# class Store(BaseModel):
#     name = models.CharField()
#     code = models.CharField()

# class Product(BaseModel):
#     product_id = models.TextField(unique=True)
#     store_id = models.ForeignKeyField(Store, backref='products')
#     name = models.TextField()
#     code = models.TextField()
#     category = models.CharField()
#     category_code = models.CharField()
#     price = models.FloatField()

from django.db import models


class Product(models.Model):
    product_id = models.IntegerField(unique=True, blank=True, null=True)
    store_id = models.IntegerField(unique=True, blank=True, null=True)
    name = models.TextField()
    code = models.TextField()
    category = models.TextField()
    category_code = models.TextField()
    price = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product'

    def __str__ (self):
        return self.name

# class Image(models.Model):
#     image = models.ImageField(upload_to='images/')
#     uploaded_at = models.DateTimeField(auto_now_add=True)