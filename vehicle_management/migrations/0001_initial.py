# Generated by Django 5.0.4 on 2024-08-13 10:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_name', models.CharField(max_length=100)),
                ('vehicle_type', models.CharField(choices=[('BIKE', 'BIKE'), ('SCOOTER', 'SCOOTER'), ('ELETRIC', 'ELETRIC')], max_length=100)),
                ('vehicle_image_front', models.ImageField(blank=True, null=True, upload_to='vehicle')),
                ('vehicle_image_back', models.ImageField(blank=True, null=True, upload_to='vehicle')),
                ('vehicle_image_left', models.ImageField(blank=True, null=True, upload_to='vehicle')),
                ('vehicle_image_right', models.ImageField(blank=True, null=True, upload_to='vehicle')),
                ('vehicle_image_speedometer', models.ImageField(blank=True, null=True, upload_to='vehicle')),
                ('price_per_day', models.IntegerField(blank=True, null=True)),
                ('price_per_week', models.IntegerField(blank=True, null=True)),
                ('price_per_month', models.IntegerField(blank=True, null=True)),
                ('bike_condition', models.CharField(blank=True, max_length=100, null=True)),
                ('category', models.CharField(blank=True, max_length=100, null=True)),
                ('theft_assurance', models.CharField(choices=[('COVERED', 'COVERED'), ('NOT COVERED', 'NOT COVERED')], max_length=100)),
                ('distance_travelled', models.IntegerField(blank=True, null=True)),
                ('last_service_date', models.DateField(blank=True, null=True)),
                ('power', models.IntegerField(blank=True, null=True)),
                ('duration', models.CharField(choices=[('DAY', 'DAY'), ('WEEK', 'WEEK'), ('MONTH', 'MONTH'), ('YEAR', 'YEAR'), ('ALL', 'ALL')], max_length=100)),
                ('discount', models.IntegerField(blank=True, null=True)),
                ('available', models.BooleanField(default=True)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
