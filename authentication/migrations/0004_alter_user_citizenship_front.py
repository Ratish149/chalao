# Generated by Django 5.0.4 on 2024-08-15 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_user_kyc_verified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='citizenship_front',
            field=models.ImageField(null=True, upload_to='citizenship'),
        ),
    ]