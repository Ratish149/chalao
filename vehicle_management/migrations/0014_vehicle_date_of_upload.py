# Generated by Django 5.0.4 on 2024-08-28 07:25

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle_management', '0013_alter_cancelbooking_remarks'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='date_of_upload',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
