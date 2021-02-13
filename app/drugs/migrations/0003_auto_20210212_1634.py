# Generated by Django 3.1.1 on 2021-02-12 13:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
        ('drugs', '0002_auto_20210212_1633'),
    ]

    operations = [
        migrations.CreateModel(
            name='Distributor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100, unique=True)),
                ('physical_address', models.CharField(max_length=120, unique=True)),
                ('postal_address', models.CharField(max_length=120, unique=True)),
                ('description', models.TextField(blank=True, max_length=100, null=True)),
                ('phone1', models.CharField(blank=True, max_length=30, null=True)),
                ('phone2', models.CharField(blank=True, max_length=30, null=True)),
                ('phone3', models.CharField(blank=True, max_length=30, null=True)),
                ('email', models.CharField(blank=True, max_length=120, null=True)),
                ('website', models.CharField(blank=True, max_length=120, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='distributor', to='users.facility')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'distributors',
            },
        ),
        migrations.AddField(
            model_name='manufacturer',
            name='distributors',
            field=models.ManyToManyField(blank=True, to='drugs.Distributor'),
        ),
    ]
