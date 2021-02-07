# Generated by Django 3.1.1 on 2021-02-06 09:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '__first__'),
        ('wholesales', '__first__'),
        ('drugs', '__first__'),
        ('retailers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RetailVariations',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('batch', models.CharField(blank=True, max_length=50, null=True)),
                ('units_per_pack', models.IntegerField(default=0)),
                ('pack_quantity', models.IntegerField(default=0)),
                ('pack_buying_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('pack_selling_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('unit_quantity', models.IntegerField(default=0)),
                ('unit_buying_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('unit_selling_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('description', models.CharField(blank=True, max_length=120, null=True)),
                ('manufacture_date', models.DateField()),
                ('expiry_date', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('distributor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='drugs.distributor')),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='retailvariations', to='users.facility')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('retail_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='retailers.retailproducts')),
                ('wholesale_product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='retail_product_images', to='wholesales.wholesaleproducts')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
