# Generated by Django 4.2.11 on 2024-05-09 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network_data', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devicedata',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
