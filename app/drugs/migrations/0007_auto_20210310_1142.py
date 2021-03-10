# Generated by Django 3.1.1 on 2021-03-10 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drugs', '0006_auto_20210310_1044'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='drugclass',
            options={},
        ),
        migrations.AlterModelOptions(
            name='drugsubclass',
            options={},
        ),
        migrations.AlterField(
            model_name='formulation',
            name='title',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterModelTable(
            name='bodysystem',
            table=None,
        ),
        migrations.AlterModelTable(
            name='drugclass',
            table=None,
        ),
        migrations.AlterModelTable(
            name='drugsubclass',
            table=None,
        ),
    ]
