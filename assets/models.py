import os
import uuid

from django.contrib.gis.db import models


def upload_image_to(instance, filename):
    filename_base, filename_ext = os.path.splitext(filename)
    return 'statics/%s%s' % (
        uuid.uuid4(),
        filename_ext
    )


class Asset(models.Model):
    id = models.BigAutoField(primary_key=True)
    image = models.ImageField(upload_to=upload_image_to, editable=True, null=True, blank=True)
