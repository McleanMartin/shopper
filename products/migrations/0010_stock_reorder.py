# Generated by Django 3.2.22 on 2023-10-29 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_stock_threshold'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='reorder',
            field=models.BooleanField(default=False),
        ),
    ]