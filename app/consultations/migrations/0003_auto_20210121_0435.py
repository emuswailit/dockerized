# Generated by Django 3.1.1 on 2021-01-21 12:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0002_prescription_is_open'),
    ]

    operations = [
        migrations.RenameField(
            model_name='prescription',
            old_name='is_open',
            new_name='is_signed',
        ),
    ]
