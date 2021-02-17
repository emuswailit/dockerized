# Generated by Django 3.1.1 on 2021-02-13 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wholesales', '0013_auto_20210213_0904'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wholesalevariations',
            old_name='available_quantity',
            new_name='quantity_available',
        ),
        migrations.RenameField(
            model_name='wholesalevariations',
            old_name='received_quantity',
            new_name='quantity_issued',
        ),
        migrations.AddField(
            model_name='wholesalevariations',
            name='quantity_received',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]