# Generated by Django 3.1.1 on 2021-02-11 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wholesales', '0029_auto_20210211_0927'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wholesalevariations',
            old_name='quantity',
            new_name='quantity_available',
        ),
        migrations.AddField(
            model_name='wholesalevariations',
            name='quantity_received',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
