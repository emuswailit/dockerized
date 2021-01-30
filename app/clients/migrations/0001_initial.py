# Generated by Django 3.1.1 on 2021-01-30 03:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '__first__'),
        ('consultations', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForwardPrescription',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('comment', models.CharField(max_length=120, null=True)),
                ('status', models.CharField(choices=[('Forwarded', 'Forwarded'), ('Quoted', 'Quoted'), ('Confirmed', 'Confirmed'), ('Partially Dispensed', 'Partally Dispensed'), ('Fully Dispensed', 'Fully Dispensed')], default='Forwarded', max_length=100)),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.facility')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('prescription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forwarded_prescription_prescription', to='consultations.prescription')),
            ],
        ),
        migrations.AddConstraint(
            model_name='forwardprescription',
            constraint=models.UniqueConstraint(fields=('facility_id', 'prescription_id'), name='forward prescription to pharmacy once'),
        ),
    ]
