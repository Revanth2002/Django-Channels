"""
ASGI config for DjangoChannels project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
import myapp.routing
from myapp.tokenauth import TokenAuthMiddleware

#DjangoChannels added
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoChannels.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": TokenAuthMiddleware(
        AuthMiddlewareStack(
        URLRouter(
            myapp.routing.websocket_urlpatterns
        )
    )
    )
})

