# Generated by Django 3.1.1 on 2021-01-31 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0007_auto_20210130_2029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prescriptionitem',
            name='duration',
            field=models.IntegerField(),
        ),
    ]
