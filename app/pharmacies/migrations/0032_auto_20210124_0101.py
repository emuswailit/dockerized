# Generated by Django 3.1.1 on 2021-01-24 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacies', '0031_auto_20210124_0100'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='payment',
            name='One transation per facility per order',
        ),
        migrations.AddConstraint(
            model_name='payment',
            constraint=models.UniqueConstraint(fields=('facility', 'order'), name='One payment per facility per order'),
        ),
    ]
