# Generated by Django 3.1.1 on 2021-01-24 05:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacies', '0020_auto_20210123_2044'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='owner',
        ),
    ]