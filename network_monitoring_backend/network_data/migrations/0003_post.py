# Generated by Django 4.2.11 on 2024-05-12 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network_data', '0002_alter_devicedata_timestamp'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
            ],
        ),
    ]
