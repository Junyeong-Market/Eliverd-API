# Generated by Django 3.0.7 on 2020-08-07 13:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0005_auto_20200805_0212'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='total',
        ),
    ]
