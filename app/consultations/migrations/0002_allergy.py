# Generated by Django 3.1.1 on 2021-01-30 04:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('consultations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Allergy',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.TextField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=100, null=True)),
                ('allergy_category', models.CharField(choices=[('Drug Allergy', 'Drug Allergy'), ('Food Allergy', 'Food Allergy'), ('Environmental Allergy', 'Environmental Allargy')], max_length=100)),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='allergy', to='users.facility')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
