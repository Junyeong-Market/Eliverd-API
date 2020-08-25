from django.contrib.gis.db import models

from account.models import User
from product.models import Product


class Store(models.Model):
    def __str__(self):
        return self.name

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False)
    description = models.TextField(null=False)
    registerer = models.ManyToManyField(User)
    registered_number = models.CharField(max_length=10, null=True)
    location = models.PointField(null=False)


class Stock(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
    price = models.PositiveIntegerField(null=False)
    amount = models.PositiveIntegerField(null=False)
