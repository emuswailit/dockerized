# Generated by Django 3.1.1 on 2021-01-30 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0009_auto_20210130_0335'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobs',
            name='advertised_positions',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='jobs',
            name='filled_positions',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='jobs',
            name='maximum_positions',
            field=models.IntegerField(default=0),
        ),
    ]
