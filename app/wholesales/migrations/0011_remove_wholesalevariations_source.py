# Generated by Django 3.1.1 on 2021-02-12 13:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wholesales', '0010_auto_20210212_1626'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wholesalevariations',
            name='source',
        ),
    ]