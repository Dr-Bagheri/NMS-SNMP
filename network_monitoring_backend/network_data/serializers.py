from rest_framework import serializers
from .models import DeviceData

class DeviceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceData
        fields = ['device_name', 'cpu_usage', 'ram_usage']