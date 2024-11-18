# Generated by Django 5.1 on 2024-11-17 10:05

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle_management', '0024_promocode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promocode',
            name='valid_from',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='promocode',
            name='valid_until',
            field=models.DateField(),
        ),
    ]