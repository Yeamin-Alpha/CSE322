# Generated by Django 5.1.2 on 2024-10-30 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0005_profile_delete_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
