# Generated by Django 3.1.1 on 2021-02-04 12:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drugs', '0007_products_sub_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='slug',
        ),
    ]