# Generated by Django 5.1 on 2024-09-22 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('careers', '0004_alter_job_remote_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='remote_type',
            field=models.CharField(choices=[('Onsite', 'Onsite'), ('Remote', 'Remote'), ('Hybrid', 'Hybrid')], max_length=100),
        ),
    ]
