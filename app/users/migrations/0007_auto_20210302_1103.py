# Generated by Django 3.1.1 on 2021-03-02 08:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='facility',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to='users.facility'),
        ),
    ]
