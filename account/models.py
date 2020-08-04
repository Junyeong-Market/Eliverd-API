import datetime
import logging
import hashlib
import uuid

from django.db import models

logger = logging.getLogger(__name__)


class User(models.Model):
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.password = hashlib.sha512(str(kwargs['password']).encode('utf-8')).hexdigest()\
            if kwargs.get('password') else self.password

    def __str__(self):
        return str(self.user_id)

    pid = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=256)
    realname = models.CharField(max_length=128, default='사용자')
    nickname = models.CharField(max_length=50, unique=True)
    is_seller = models.BooleanField(null=False, default=False)


class Session(models.Model):

    def __init__(self, *args, **kwargs):
        super(Session, self).__init__(*args, **kwargs)
        expire = datetime.datetime.now()
        expire += datetime.timedelta(years=1)
        self.expireAt = expire

    def __str__(self):
        return str(self.id)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pid = models.ForeignKey(User, on_delete=models.CASCADE)
    expireAt = models.DateTimeField()
