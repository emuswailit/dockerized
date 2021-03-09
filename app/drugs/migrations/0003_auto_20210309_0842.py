# Generated by Django 3.1.1 on 2021-03-09 05:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diseases', '0002_remove_management_drug'),
        ('drugs', '0002_contraindications'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='indications',
            name='indication',
        ),
        migrations.AddField(
            model_name='indications',
            name='disease',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='diseases.diseases'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='indications',
            name='dose',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
