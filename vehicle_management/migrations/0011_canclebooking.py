# Generated by Django 5.1 on 2024-08-21 09:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle_management', '0010_extendbooking'),
    ]

    operations = [
        migrations.CreateModel(
            name='CancleBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remarks', models.TextField()),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vehicle_management.booking')),
            ],
        ),
    ]
