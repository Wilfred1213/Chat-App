from django.urls import path
from chat.consumers import ChatConsumer, PrivateChatConsumer

websocket_urlpatterns = [
    path("ws/chat/<str:room_name>/", ChatConsumer.as_asgi()),
    path("ws/private_chat/<str:friend_username>/", PrivateChatConsumer.as_asgi()),
]
