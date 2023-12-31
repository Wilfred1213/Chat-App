# """
# ASGI config for chatapp project.

# It exposes the ASGI callable as a module-level variable named ``application``.

# For more information on this file, see
# https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
# """
"""
ASGI config for authentication project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatapp.settings')

import django
django.setup()
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack  # new import
from channels.routing import ProtocolTypeRouter, URLRouter


import chatapp.routing

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatapp.settings')



application = ProtocolTypeRouter({
  'http': get_asgi_application(),
  'websocket': AuthMiddlewareStack( 
        URLRouter(
            chatapp.routing.websocket_urlpatterns
        )
    ), 
})
# if __name__ == "__main__":
#     from daphne.cli import CommandLineInterface
#     CommandLineInterface().run()


# import os
# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.core.asgi import get_asgi_application

# import chatapp.routing

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatapp.settings')

# application = ProtocolTypeRouter({
#     'http': get_asgi_application(),
#     'websocket': URLRouter(chatapp.routing.websocket_urlpatterns),
# })

# if __name__ == "__main__":
#     from daphne.cli import CommandLineInterface
#     CommandLineInterface().run()


# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.core.asgi import get_asgi_application

# import chatapp.routing

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatapp.settings')

# application = ProtocolTypeRouter({
#   'http': get_asgi_application(),
#   'websocket': URLRouter(
#       chatapp.routing.websocket_urlpatterns
#     ),
# })





# # asgi.py

# import os
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatapp.settings')

# # Import your routing configuration correctly
# from chatapp.routing import websocket_urlpatterns

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(websocket_urlpatterns)
#     ),
# })

