# Generated by Django 5.1 on 2024-11-12 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle_management', '0021_delete_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='price',
            field=models.JSONField(blank=True, null=True),
        ),
    ]