# Generated by Django 5.1.2 on 2025-04-25 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0004_booking_hours_booking_total_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
    ]
