# Generated by Django 3.0.7 on 2020-09-06 12:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_user_home'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_seller',
        ),
    ]
