# Generated by Django 3.0.6 on 2020-06-15 11:16

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_auto_20200602_0926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='id',
            field=models.CharField(default=uuid.UUID('3356d747-53bc-4170-80ea-158f8ea655ca'), max_length=100, primary_key=True, serialize=False, unique=True),
        ),
    ]
