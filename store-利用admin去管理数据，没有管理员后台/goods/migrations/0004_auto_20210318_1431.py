# Generated by Django 2.2 on 2021-03-18 06:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0003_auto_20210318_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='create_date',
            field=models.DateField(default=datetime.datetime(2021, 3, 18, 14, 31, 26, 753672)),
        ),
    ]
