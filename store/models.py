from django.db import models
from django.contrib.gis.db import models as geo_models

from account.models import User
from product.models import Product


class Store(geo_models.Model):
    def __str__(self):
        return self.name

    id = geo_models.AutoField(primary_key=True)
    name = geo_models.CharField(max_length=50, null=False)
    description = geo_models.TextField(null=False)
    registerer = geo_models.ForeignKey(User, on_delete=geo_models.CASCADE)
    registered_number = geo_models.CharField(max_length=10)
    location = geo_models.PointField(null=False)
    products = geo_models.ManyToManyField(Product)

