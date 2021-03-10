# Generated by Django 3.1.1 on 2021-03-09 11:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('diseases', '0003_auto_20210309_1124'),
    ]

    operations = [
        migrations.CreateModel(
            name='Symptoms',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.TextField(max_length=120)),
                ('description', models.TextField(blank=True, max_length=100, null=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('disease', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='diseases.diseases')),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='symptoms', to='users.facility')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='SignsAndSymptoms',
        ),
    ]
