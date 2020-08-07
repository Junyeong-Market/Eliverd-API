from django.db import models
from django.db.models import Sum

from account.models import User
from store.models import Stock, Store


class TransactionStatus(models.TextChoices):
    PENDING = 'pending'
    PROCESSED = 'processed'
    CANCELED = 'canceled'
    FAILED = 'failed'


class OrderStatus(models.TextChoices):
    PENDING = 'pending'
    READY = 'ready'
    DELIVERING = 'delivering'
    DELIVERED = 'delivered'
    CANCELED = 'canceled'
    DONE = 'done'


class StockAppliedStatus(models.IntegerChoices):
    PREPARED = 0
    APPLIED = 1
    FAILED = 2


class OrderedStock(models.Model):
    def __str__(self):
        return self.stock.product.name + ' x ' + str(self.amount)

    osid = models.AutoField(primary_key=True)
    stock = models.ForeignKey(Stock, models.CASCADE)
    amount = models.PositiveIntegerField()
    status = models.PositiveIntegerField(choices=StockAppliedStatus.choices, default=StockAppliedStatus.PREPARED)


class PartialOrder(models.Model):

    poid = models.AutoField(primary_key=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    status = models.CharField(choices=OrderStatus.choices, max_length=16, default=OrderStatus.PENDING)
    stocks = models.ManyToManyField(OrderedStock)


class Order(models.Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    oid = models.AutoField(primary_key=True)
    tid = models.CharField(max_length=20, unique=True, null=True)
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    partials = models.ManyToManyField(PartialOrder)
    status = models.CharField(choices=TransactionStatus.choices, max_length=16, default=TransactionStatus.PENDING)

    def get_total(self):
        return self.partials.aggregate(Sum('stocks__stock__price'))['stocks__stock__price__sum']
