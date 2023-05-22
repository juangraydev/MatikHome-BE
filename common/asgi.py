import os


from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import devices.routing

os.environ.setdefault('DJANG_SETTING_MODULE', 'common.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(devices.routing.websocket_urlpatterns)
    )
})