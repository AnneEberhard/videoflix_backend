# Generated by Django 5.0.3 on 2024-04-16 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='address',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='custom',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
