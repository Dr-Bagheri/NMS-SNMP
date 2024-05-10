from timescale.db.models import Model
from timescale.db.models.fields import TimescaleDateTimeField, FloatField, CharField, TextField, IntegerField

class DeviceData(Model):
    timestamp = TimescaleDateTimeField(auto_now_add=True)
    device_name = CharField(max_length=255)
    cpu_usage = FloatField()
    ram_usage = FloatField()
    device_ip = CharField(max_length=255)  
    device_id = IntegerField()  
    class Meta:
        # This orders the data by 'timestamp' descending, so newest entries first
        ordering = ['-timestamp']

class Post(Model):
    
    title = CharField(max_length=255)
    content = TextField()
