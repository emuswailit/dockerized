# Generated by Django 3.1.1 on 2021-02-02 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drugs', '0011_auto_20210202_0036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contraindications',
            name='title',
            field=models.TextField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
