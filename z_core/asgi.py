from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'z_core.settings')

django_asgi_app = get_asgi_application()

from z_chat import routing as chat_routing
from z_users import routing as users_routing

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                chat_routing.websocket_urlpatterns + users_routing.websocket_urlpatterns
            )
        )
    )
})
