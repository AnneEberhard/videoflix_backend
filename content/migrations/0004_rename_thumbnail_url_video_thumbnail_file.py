# Generated by Django 5.0.3 on 2024-04-06 06:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_video_thumbnail_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='thumbnail_url',
            new_name='thumbnail_file',
        ),
    ]
