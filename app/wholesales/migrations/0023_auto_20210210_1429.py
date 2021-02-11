# Generated by Django 3.1.1 on 2021-02-10 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wholesales', '0022_remove_despatchitems_wholesale_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='despatchitems',
            name='batch',
            field=models.CharField(blank=True, max_length=140, null=True),
        ),
        migrations.AddField(
            model_name='despatchitems',
            name='wholesaler_confirmed',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='despatches',
            name='courier_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='despatches',
            name='despatch_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='despatches',
            name='receipt_confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
