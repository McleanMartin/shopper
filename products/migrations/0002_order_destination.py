# Generated by Django 3.2.22 on 2023-11-06 00:59

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='destination',
            field=models.CharField(default=datetime.datetime(2023, 11, 6, 0, 59, 12, 529856, tzinfo=utc), max_length=200),
            preserve_default=False,
        ),
    ]
