# Generated by Django 3.1.1 on 2021-03-07 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drugs', '0010_remove_products_sub_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drugclass',
            name='title',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
