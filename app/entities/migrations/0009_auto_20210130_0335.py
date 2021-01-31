# Generated by Django 3.1.1 on 2021-01-30 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0008_auto_20210130_0317'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='jobs',
            constraint=models.UniqueConstraint(fields=('facility', 'title'), name='Title to be unique per facility'),
        ),
    ]
