# Generated by Django 3.1.1 on 2021-01-24 04:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacies', '0019_order_orderitem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='is_checked_out',
            new_name='is_open',
        ),
    ]