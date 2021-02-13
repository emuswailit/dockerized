# Generated by Django 3.1.1 on 2021-02-12 13:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drugs', '0005_auto_20210212_1641'),
        ('wholesales', '0011_remove_wholesalevariations_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='wholesalevariations',
            name='source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='listing_purchases', to='drugs.distributor'),
        ),
    ]
