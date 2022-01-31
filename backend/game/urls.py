from django.urls import path, include
from rest_framework import routers

from game.views import GameViewSet

app_name = 'game'

router = routers.SimpleRouter()
router.register('games', GameViewSet)
urlpatterns = [
    path('', include(router.urls)),
]
