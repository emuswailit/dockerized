# Generated by Django 3.1.1 on 2021-01-27 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_enterprises_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enterprises',
            name='title',
            field=models.CharField(max_length=120, unique=True),
        ),
    ]