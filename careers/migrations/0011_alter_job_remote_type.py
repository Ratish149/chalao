# Generated by Django 5.1 on 2024-09-27 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('careers', '0010_alter_job_remote_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='remote_type',
            field=models.CharField(choices=[('Onsite', 'Onsite'), ('Hybrid', 'Hybrid'), ('Remote', 'Remote')], max_length=100),
        ),
    ]