# Generated by Django 3.1.1 on 2021-02-04 13:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('drugs', '0010_auto_20210204_0438'),
        ('users', '0002_auto_20210204_0501'),
        ('wholesales', '0002_auto_20210204_0530'),
    ]

    operations = [
        migrations.CreateModel(
            name='WholesaleProducts',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wholesaleproducts', to='users.facility')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listing_owner', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='listing_products', to='drugs.products')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='wholesalevariations',
            name='listing',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='listing_purchases', to='wholesales.wholesaleproducts'),
        ),
        migrations.DeleteModel(
            name='Listings',
        ),
    ]
