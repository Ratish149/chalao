# Generated by Django 5.1 on 2024-09-22 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle_management', '0016_alter_vehicle_vehicle_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='category',
            field=models.CharField(blank=True, choices=[('BUDGET', 'BUDGET'), ('PREMIUM', 'PREMIUM'), ('ELETRIC', 'ELETRIC')], max_length=100, null=True),
        ),
    ]
