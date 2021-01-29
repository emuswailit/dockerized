# Generated by Django 3.1.1 on 2021-01-28 12:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0005_auto_20210127_2332'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0009_facility_trial_done'),
        ('entities', '0002_departmentalcharges'),
        ('consultations', '0005_merge_20210128_0416'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppointmentPayments',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('narrative', models.CharField(max_length=300)),
                ('reference', models.CharField(max_length=120)),
                ('status', models.CharField(choices=[('PENDING', 'PENDING'), ('SUCCESS', 'SUCCESS'), ('FAILED', 'FAILED')], default='PENDING', max_length=120)),
                ('subscription_created', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveConstraint(
            model_name='appointments',
            name='One patient per appointment slot',
        ),
        migrations.RemoveField(
            model_name='appointments',
            name='dependant',
        ),
        migrations.RemoveField(
            model_name='appointments',
            name='slot',
        ),
        migrations.AddField(
            model_name='slots',
            name='employee',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='slot_employee', to='entities.employees'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='appointmentpayments',
            name='dependant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointment_dependant', to='users.dependant'),
        ),
        migrations.AddField(
            model_name='appointmentpayments',
            name='facility',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointmentpayments', to='users.facility'),
        ),
        migrations.AddField(
            model_name='appointmentpayments',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appointmentpayments',
            name='payment_method',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payments.paymentmethods'),
        ),
        migrations.AddField(
            model_name='appointmentpayments',
            name='slot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='consultations.slots'),
        ),
        migrations.AddField(
            model_name='appointments',
            name='appointment_payment',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, related_name='appointment_slot', to='consultations.appointmentpayments'),
            preserve_default=False,
        ),
    ]
