# Generated by Django 3.1.1 on 2021-01-22 09:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacies', '0009_auto_20210122_0108'),
    ]

    operations = [
        migrations.RenameField(
            model_name='prescriptionquote',
            old_name='prescription',
            new_name='forward_prescription',
        ),
    ]
