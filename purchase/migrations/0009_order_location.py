# Generated by Django 3.0.7 on 2020-08-25 02:12

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0008_partialorder_is_delivery'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(null=True, srid=4326),
        ),
    ]
