# Generated by Django 3.1.1 on 2021-01-30 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drugs', '0001_initial'),
        ('consultations', '0002_allergy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointmentconsultations',
            name='current_medication',
            field=models.ManyToManyField(blank=True, null=True, to='drugs.Generic'),
        ),
    ]
