# Generated by Django 5.1 on 2024-10-15 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('careers', '0016_alter_job_remote_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='remote_type',
            field=models.CharField(choices=[('Remote', 'Remote'), ('Hybrid', 'Hybrid'), ('Onsite', 'Onsite')], max_length=100),
        ),
    ]
