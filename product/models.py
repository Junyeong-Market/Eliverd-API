import uuid

from django.db import models


class Manufacturer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)


class Category(models.TextChoices):
    FASHION = 'fashion'
    BEAUTY = 'beauty'
    BABY = 'baby'
    FOOD = 'food'
    KITCHEN = 'kitchen'
    LIVING = 'living'
    FURNITURE = 'furniture'
    DIGITAL = 'digital'
    LEISURE = 'leisure'
    CAR = 'car'
    PUBLICATION = 'publication'
    TOY = 'toy'
    OFFICE = 'office'
    PET = 'pet'
    HEALTH = 'health'


class Product(models.Model):
    def __str__(self):
        return self.name

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, null=False)
    manufacturer = models.ForeignKey(Manufacturer, models.CASCADE)
    category = models.CharField(choices=Category.choices, max_length=32)
    ian = models.CharField(max_length=36, default=uuid.uuid4)  # International Article Number == 바코드

