# Generated by Django 5.1 on 2024-08-21 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle_management', '0012_rename_canclebooking_cancelbooking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cancelbooking',
            name='remarks',
            field=models.TextField(blank=True, null=True),
        ),
    ]
