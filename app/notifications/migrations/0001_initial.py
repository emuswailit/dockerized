# Generated by Django 3.1.1 on 2021-01-21 10:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('current_bid', models.FloatField()),
                ('bid_count', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('live_date', models.DateTimeField()),
                ('expiry_date', models.DateTimeField()),
                ('active', models.BooleanField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('email_sent', models.BooleanField(default=False)),
                ('email_sent_time', models.DateTimeField(blank=True, null=True)),
                ('auction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notifications.auction')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmailQueue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('auction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='notifications.auction')),
                ('bid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='notifications.bid')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
