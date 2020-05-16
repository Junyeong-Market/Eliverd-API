import datetime
import uuid

from django.db import models

# Create your models here.


class User(models.Model):
    def __str__(self):
        return str(self.id)

    pid = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=64)
    nickname = models.CharField(max_length=50, unique=True)
    isSeller = models.BooleanField(null=False, default=False)


class Session(models.Model):

    def __init__(self):
        super(Session, self).__init__()
        expire = datetime.datetime.now()
        expire.replace(day=expire.day+3)
        self.expireAt = expire

    def __str__(self):
        return str(self.id)

    id = models.CharField(max_length=100, unique=True, primary_key=True, default=uuid.uuid4())
    pid = models.ForeignKey(User, to_field=User.pid, on_delete=models.CASCADE)
    expireAt = models.DateTimeField()
