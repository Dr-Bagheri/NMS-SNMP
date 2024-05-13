import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
import network_monitoring_backend.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'network_monitoring_backend.settings')




application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            network_monitoring_backend.routing.websocket_urlpatterns
            
        )
    ),
})

