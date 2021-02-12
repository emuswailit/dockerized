# Generated by Django 3.1.1 on 2021-02-12 08:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wholesales', '0005_auto_20210212_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='retaileraccounts',
            name='placement_limit',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='retaileraccounts',
            name='retailer_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='retaileraccounts',
            name='retailer_verified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='retailer_verifier', to=settings.AUTH_USER_MODEL),
        ),
    ]
