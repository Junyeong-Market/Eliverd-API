import logging
from datetime import datetime

from django.contrib.gis.db import models
from django.db.models.functions import Now
from django.utils import timezone

from account.models import User
from store.models import Stock, Store

logger = logging.getLogger(__name__)


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
    destination = models.PointField(null=True)
    transport = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_created=True, default=timezone.now)


class Order(models.Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    oid = models.AutoField(primary_key=True)
    tid = models.CharField(max_length=20, unique=True, null=True)
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    partials = models.ManyToManyField(PartialOrder)
    status = models.CharField(choices=TransactionStatus.choices, max_length=16, default=TransactionStatus.PENDING)
    destination = models.PointField(null=True)
    created_at = models.DateTimeField(auto_created=True, default=timezone.now)
    exclude = models.BooleanField(default=False)

    def get_total(self):
        total = 0
        for partial in self.partials.all():
            for stock in partial.stocks.all():
                total += stock.amount * stock.stock.price
        return total

    def get_order_name(self):
        first_name = self.partials.filter().first().store.name
        count = self.partials.count()
        return f"{first_name} 포함 {count}개 상점에 주문" if count > 1 else f"{first_name}에 주문"
