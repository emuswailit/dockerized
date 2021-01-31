# Generated by Django 3.1.1 on 2021-01-30 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0005_auto_20210130_0031'),
    ]

    operations = [
        migrations.AddField(
            model_name='designation',
            name='is_advertised',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='designation',
            name='is_vacant',
            field=models.BooleanField(default=True),
        ),
    ]
