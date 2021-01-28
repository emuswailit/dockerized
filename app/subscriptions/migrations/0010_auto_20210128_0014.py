# Generated by Django 3.1.1 on 2021-01-28 08:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20210127_0117'),
        ('payments', '0005_auto_20210127_2332'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('subscriptions', '0009_auto_20210127_2356'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionPayments',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('narrative', models.CharField(max_length=300)),
                ('reference', models.CharField(max_length=120)),
                ('status', models.CharField(choices=[('PENDING', 'PENDING'), ('SUCCESS', 'SUCCESS'), ('FAILED', 'FAILED')], default='PENDING', max_length=120)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptionpayments', to='users.facility')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('payment_method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payments.paymentmethods')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscriptions.plan')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='subscription',
            name='subscription_payment',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='subscriptions.subscriptionpayments'),
        ),
        migrations.DeleteModel(
            name='SubscriptionPayment',
        ),
    ]
