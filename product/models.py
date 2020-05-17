from django.db import models


class Manufacturer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)


class Product(models.Model):
    def __str__(self):
        return self.name

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, null=False)
    manufacturer = models.ForeignKey(Manufacturer, models.CASCADE)
    ian = models.CharField(max_length=17, null=True)  # International Article Number == 바코드

