# Generated by Django 3.0.7 on 2020-08-07 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0006_remove_order_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_delivery',
            field=models.BooleanField(default=True),
        ),
    ]
