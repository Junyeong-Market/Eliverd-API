from django.db import models

# Create your models here.
from django.db.models import Sum

from store.models import Stock, Store


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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.total = self.stocks.aggregate(Sum('stock__price'))

    oid = models.AutoField(primary_key=True)
    tid = models.CharField(max_length=20, unique=True, null=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    stocks = models.ManyToManyField(OrderedStock)
    status = models.CharField(choices=OrderStatus.choices, max_length=16, default=OrderStatus.PENDING)
    total = models.PositiveIntegerField(null=True)
