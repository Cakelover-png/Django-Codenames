from django.contrib.auth.models import User
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from django_codenames.utils.serializers import SerializerFactory
from game.choices import GameStatus
from game.models import Game
from game.serializers import CreateGameSerializer, ListGameSerializer


class GameViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = Game.objects.select_related('creator').filter(status=GameStatus.PENDING).order_by('-created')
    serializer_class = SerializerFactory(create=CreateGameSerializer,
                                         default=ListGameSerializer)
    permission_classes = [IsAuthenticated]

    @action(methods=['POST'], detail=False)
    def join_game(self, request, *_, **__):
        user = request.user
        game = Game.objects.filter(pk=request.data.get('pk')).first()
        if not game:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        game.players_in_lobby.add(user)
        return Response(status=status.HTTP_200_OK)

