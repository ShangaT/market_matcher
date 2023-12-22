from django.db import models


class Store(models.Model):
    name = models.CharField()
    code = models.CharField()

    class Meta:
        db_table = 'store'


class Region(models.Model):
    name = models.CharField()

    class Meta:
        db_table = 'region'


class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    product_id = models.TextField(unique=True)
    name = models.TextField()
    code = models.TextField()
    category = models.CharField()
    category_code = models.CharField()
    price = models.FloatField()

    class Meta:
        db_table = 'product'
