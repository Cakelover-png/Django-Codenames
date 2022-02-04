from django.urls import re_path

from game import consumers

websocket_urlpatterns = [
    re_path('ws/game/game/', consumers.GameConsumer.as_asgi()),
]
