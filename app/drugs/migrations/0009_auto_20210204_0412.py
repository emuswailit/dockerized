# Generated by Django 3.1.1 on 2021-02-04 12:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('drugs', '0008_remove_products_slug'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='products',
            unique_together={('facility', 'title', 'preparation')},
        ),
    ]
