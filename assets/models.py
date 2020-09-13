import logging
import os

from django.contrib.gis.db import models
from django.utils.timezone import now

logger = logging.getLogger(__name__)


def upload_image_to(instance, filename):
    filename_base, filename_ext = os.path.splitext(filename)
    return 'statics/%s/%s' % (
        now().strftime("%Y%m%d"),
        instance.id
    )


class Asset(models.Model):
    id = models.BigAutoField(primary_key=True)
    image = models.ImageField(upload_to=upload_image_to, editable=True, null=True, blank=True)
