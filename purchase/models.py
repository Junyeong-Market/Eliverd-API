from django.db import models

# Create your models here.
from store.models import Stock


class OrderStatus(models.TextChoices):
    PENDING = "pending"
    PROCESSED = "processed"
    CANCELED = "canceled"
    FAILED = "failed"


class OrderedStock(models.Model):
    def __str__(self):
        return self.stock.product.name + ' x ' + str(self.amount)

    osid = models.AutoField(primary_key=True)
    stock = models.ForeignKey(Stock, models.CASCADE)
    amount = models.PositiveIntegerField()


class Order(models.Model):
    oid = models.AutoField(primary_key=True)
    tid = models.CharField(max_length=20, unique=True)
    stocks = models.ManyToManyField(OrderedStock)
    status = models.CharField(choices=OrderStatus.choices, max_length=16)
