# Generated by Django 3.1.1 on 2021-02-01 05:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacies', '0006_prescriptionquote_payment_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pharmacypayment',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payment_order', to='pharmacies.order'),
        ),
    ]