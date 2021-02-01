# Generated by Django 3.1.1 on 2021-01-31 04:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0005_auto_20210130_1957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointmentconsultations',
            name='appointment',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='patient_consultation_appointment', to='consultations.appointments'),
        ),
    ]