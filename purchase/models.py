from django.db import models

# Create your models here.
from store.models import Stock


class OrderedStock(models.Model):
    def __str__(self):
        return self.stock.product.name + ' x ' + str(self.amount)

    osid = models.AutoField(primary_key=True)
    stock = models.ForeignKey(Stock, models.CASCADE)
    amount = models.PositiveIntegerField()
