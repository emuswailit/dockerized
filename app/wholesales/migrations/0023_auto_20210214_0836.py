# Generated by Django 3.1.1 on 2021-02-14 05:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wholesales', '0022_auto_20210214_0827'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoiceitems',
            name='wholesale_variation',
        ),
        migrations.AddField(
            model_name='invoiceitems',
            name='requisition_item',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='requisition_item', to='wholesales.requisitionitems'),
            preserve_default=False,
        ),
    ]
