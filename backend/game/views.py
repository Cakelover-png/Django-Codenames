from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from django_codenames.utils.serializers import SerializerFactory
from game.models import Game
from game.serializers import CreateGameSerializer, ListGameSerializer


class GameViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = Game.objects.select_related('creator')
    serializer_class = SerializerFactory(create=CreateGameSerializer,
                                         default=ListGameSerializer)
    permission_classes = [IsAuthenticated]
