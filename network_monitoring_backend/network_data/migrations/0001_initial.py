# Generated by Django 4.2.11 on 2024-05-09 16:53

from django.db import migrations, models
import timescale.db.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', timescale.db.models.fields.TimescaleDateTimeField(interval='1 day')),
                ('device_name', models.CharField(max_length=255)),
                ('cpu_usage', models.FloatField()),
                ('ram_usage', models.FloatField()),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]