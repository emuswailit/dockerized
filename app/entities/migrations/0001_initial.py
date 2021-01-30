# Generated by Django 3.1.1 on 2021-01-30 03:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import entities.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=120, unique=True)),
                ('description', models.CharField(max_length=300, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('open_monday', models.BooleanField(default=False)),
                ('open_tuesday', models.BooleanField(default=False)),
                ('open_wednesday', models.BooleanField(default=False)),
                ('open_thursday', models.BooleanField(default=False)),
                ('open_friday', models.BooleanField(default=False)),
                ('open_saturday', models.BooleanField(default=False)),
                ('open_sunday', models.BooleanField(default=False)),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='department', to='users.facility')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='department_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Employees',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('designation', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_superintendent', models.BooleanField(default=False)),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employee_department', to='entities.department')),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='users.facility')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='facility_admin_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('basic_salary', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('house_allowance', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('risk_allowance', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('uniform_allowance', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='entities.employees')),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='salary', to='users.facility')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='salary_owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Professionals',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_available', models.BooleanField(default=True)),
                ('is_verified', models.BooleanField(default=True)),
                ('certificate', models.FileField(upload_to=entities.models.professional_certificate_upload_to)),
                ('national_id', models.FileField(upload_to=entities.models.professional_licence_upload_to)),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('cadre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='professionals_professions', to='users.cadres')),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='professionals', to='users.facility')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='professional_owner', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='professional_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProfessionalAnnualLicence',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('annual_licence', models.ImageField(upload_to=entities.models.professional_annual_licence_upload_to)),
                ('expires_on', models.DateField()),
                ('is_current', models.BooleanField(default=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='professionalannuallicence', to='users.facility')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('professional', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='professional_annual_licence_professional', to='entities.professionals')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='employees',
            name='professional',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_professional', to='entities.professionals'),
        ),
        migrations.CreateModel(
            name='DepartmentalCharges',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('consultation_fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('other_charges', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('department', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='entities.department')),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departmentalcharges', to='users.facility')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departmental_charges_owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddConstraint(
            model_name='employees',
            constraint=models.UniqueConstraint(fields=('facility', 'professional'), name='Professional can only be employed once in a facility'),
        ),
        migrations.AddConstraint(
            model_name='department',
            constraint=models.UniqueConstraint(fields=('facility', 'title'), name='Unique department title in each facility'),
        ),
    ]
