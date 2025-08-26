
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from config.urls.websocket_url.websocket_urls import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": get_asgi_application(), 
    "websocket": AuthMiddlewareStack(
        URLRouter( websocket_urlpatterns )
    ),
})
