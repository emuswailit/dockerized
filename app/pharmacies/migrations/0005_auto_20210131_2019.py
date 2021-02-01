# Generated by Django 3.1.1 on 2021-02-01 04:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0002_cadres_cluster'),
        ('pharmacies', '0004_remove_quoteitem_item_cost'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='is_confirmed',
            new_name='client_confirmed',
        ),
        migrations.AddField(
            model_name='order',
            name='pharmacist_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='client_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='pharmacist_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='quoteitem',
            name='client_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='quoteitem',
            name='pharmacist_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='PharmacyPayment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('reference', models.CharField(blank=True, max_length=120, null=True)),
                ('status', models.CharField(choices=[('PENDING', 'PENDING'), ('SUCCESS', 'SUCCESS'), ('FAILED', 'FAILED')], default='PENDING', max_length=120)),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_facility', to='users.facility')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_order', to='pharmacies.order')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pharmacy_payment_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='pharmacypayment',
            constraint=models.UniqueConstraint(fields=('facility', 'order'), name='One payment per facility per order'),
        ),
    ]
