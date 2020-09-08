from django.contrib.gis.db import models


def upload_image_to(instance, filename):
    import os
    from django.utils.timezone import now
    filename_base, filename_ext = os.path.splitext(filename)
    return 'posts/%s/%s' % (
        now().strftime("%Y%m%d"),
        instance.id
    )


class Asset(models.Model):
    id = models.BigAutoField(primary_key=True)
    image = models.ImageField(upload_to=upload_image_to, editable=True, null=True, blank=True)
