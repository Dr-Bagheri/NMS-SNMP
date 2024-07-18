from django.apps import AppConfig
from threading import Thread
import time

class NetworkDataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'network_data'

    def ready(self):
        if not hasattr(self, 'collector_thread'):
            self.collector_thread = Thread(target=self.start_snmp_collector, daemon=True)
            self.collector_thread.start()

    def start_snmp_collector(self):
        from network_data.snmp_collector import run_anomaly_detection
        while True:
            run_anomaly_detection()
            time.sleep(1)  # Ensures it runs approximately every second