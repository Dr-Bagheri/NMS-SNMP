from django.urls import re_path
from network_monitoring_backend.consumers import SNMPConsumer

websocket_urlpatterns = [
    re_path(r'^ws/snmp/$', SNMPConsumer.as_asgi()),
]

