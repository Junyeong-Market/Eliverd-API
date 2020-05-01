from django.db import models

# Create your models here.


class User(models.Model):
    def __str__(self):
        return str(self.id)

    pid = models.AutoField(primary_key=True)
    id = models.CharField(unique=True)
    password = models.CharField(max_length=64)
    nickname = models.CharField(unique=True)
    isSeller = models.BooleanField(null=False, default=False)

