# Generated by Django 3.1.1 on 2021-01-30 08:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0003_auto_20210130_0022'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employees',
            name='description',
        ),
    ]