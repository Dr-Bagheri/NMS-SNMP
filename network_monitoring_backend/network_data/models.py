from django.db import models
from timescale.db.models.fields import TimescaleDateTimeField

class DeviceData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set the timestamp on record creation
    device_name = models.CharField(max_length=255)
    cpu_usage = models.FloatField()
    ram_usage = models.FloatField()

    class Meta:
        # This orders the data by 'timestamp' descending, so newest entries first
        ordering = ['-timestamp']

class Post(models.Model):
    
    title = models.CharField(max_length=255)
    content = models.TextField()