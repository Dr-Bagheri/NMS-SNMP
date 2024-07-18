from django.db import models

class DeviceData(models.Model):
    timestamp = models.DateTimeField()
    ifInOctets = models.FloatField()
    ifOutOctets = models.FloatField()
    ipInReceives = models.FloatField()
    ipOutRequests = models.FloatField()
    tcpInSegs = models.FloatField()
    tcpOutSegs = models.FloatField()
    udpInDatagrams = models.FloatField()
    udpOutDatagrams = models.FloatField()
    ifInDiscards = models.FloatField()
    ifOutDiscards = models.FloatField()
    ifInErrors = models.FloatField()
    ifOutErrors = models.FloatField()
    ifSpeed = models.FloatField()
    sysUpTime = models.FloatField()
    ifOperStatus = models.IntegerField()
    ifLastChange = models.FloatField()
    hrProcessorLoad = models.FloatField()
    hrMemorySize = models.FloatField()
    hrStorageUsed = models.FloatField()
    anomaly_type = models.CharField(max_length=50)
    predicted_label = models.IntegerField()

    def __str__(self):
        return f"Device Data at {self.timestamp}"