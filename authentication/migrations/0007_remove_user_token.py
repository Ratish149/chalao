# Generated by Django 5.0.4 on 2024-08-26 07:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_user_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='token',
        ),
    ]
