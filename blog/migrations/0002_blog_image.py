# Generated by Django 5.1 on 2024-09-27 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='image',
            field=models.ImageField(default=1, upload_to='blog_images/'),
            preserve_default=False,
        ),
    ]