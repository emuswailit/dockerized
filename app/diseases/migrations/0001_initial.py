# Generated by Django 3.1.1 on 2021-02-12 05:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('drugs', '__first__'),
        ('users', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Diseases',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.TextField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, max_length=100, null=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diseases', to='users.facility')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Sources',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.TextField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('disease', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='diseases.diseases')),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sources', to='users.facility')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SignsAndSymptoms',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.TextField(max_length=120)),
                ('description', models.TextField(blank=True, max_length=100, null=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('disease', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='diseases.diseases')),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='signsandsymptoms', to='users.facility')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Prevention',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.TextField(blank=True, max_length=120, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('disease', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='diseases.diseases')),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prevention', to='users.facility')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Management',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('treatment_category', models.CharField(choices=[('Drug Management', 'Drug Management'), ('Non-Drug Management', 'Non-Drug Management')], max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('disease', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='diseases.diseases')),
                ('drug', models.ForeignKey(max_length=100, on_delete=django.db.models.deletion.CASCADE, to='drugs.generic')),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='management', to='users.facility')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DiseaseStages',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.TextField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('disease', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='diseases.diseases')),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diseasestages', to='users.facility')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DiseaseStageCategories',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, max_length=100, null=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('disease_stage', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='diseases.diseasestages')),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diseasestagecategories', to='users.facility')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DiseaseNotes',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.TextField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, max_length=100, null=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('disease', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='diseases.diseases')),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diseasenotes', to='users.facility')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DifferentialDiagnosis',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.TextField(max_length=120)),
                ('description', models.TextField(blank=True, null=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('disease', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='diseases.diseases')),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='differentialdiagnosis', to='users.facility')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Diagnosis',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.TextField(max_length=120)),
                ('description', models.TextField(blank=True, null=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('disease', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='diseases.diseases')),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diagnosis', to='users.facility')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
