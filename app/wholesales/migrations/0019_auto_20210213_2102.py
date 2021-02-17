# Generated by Django 3.1.1 on 2021-02-13 18:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
        ('wholesales', '0018_requisitions_total_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requisitionpayments',
            name='payment_terms',
        ),
        migrations.AddField(
            model_name='requisitionpayments',
            name='invoice',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='requisition_payment_invoice', to='wholesales.requisitions'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='requisitionpayments',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requisition_payment_owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('invoice_type', models.CharField(choices=[('CASH', 'CASH'), ('CREDIT', 'CREDIT'), ('PLACEMENT', 'PLACEMENT')], max_length=100)),
                ('total_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('paid_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('due_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoice', to='users.facility')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoice_owner', to=settings.AUTH_USER_MODEL)),
                ('requisition', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='invoice_requisition', to='wholesales.requisitions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]