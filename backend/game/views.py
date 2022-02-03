from django.utils.translation import gettext_lazy as lz

from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from django_codenames.utils.serializers import SerializerFactory
from game.choices import TeamType, GameStatus
from game.models import Game, GameCard
from game.serializers import CreateGameSerializer, ListGameSerializer, RetrieveGameSerializer, \
    CreateFieldOperativeSerializer, CreateSpymasterSerializer
from game.utils.custom_functions import shuffled_game_cards, set_finished_if_winner


class GameViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = Game.objects.select_related('creator')
    serializer_class = SerializerFactory(create=CreateGameSerializer,
                                         retrieve=RetrieveGameSerializer,
                                         default=ListGameSerializer)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super(GameViewSet, self).get_queryset()
        if self.action == 'retrieve':
            qs = qs.prefetch_related('fieldoperative__player', 'spymaster__player', 'game_cards__card')
        return qs

    def get_serializer_context(self):
        context = {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }
        if self.action in ('become_field_operative', 'become_spymaster'):
            context['game'] = self.get_object()
        return context

    @action(detail=True, methods=('POST',))
    def join_game(self, request, *_, **__):
        game: Game = self.get_object()
        game.players_in_lobby.add(request.user)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=('POST',))
    def leave_game(self, request, *_, **__):
        game: Game = self.get_object()
        game.players_in_lobby.remove(request.user)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=('POST',), serializer_class=CreateFieldOperativeSerializer)
    def become_field_operative(self, request, *_, **__):
        return self.create(request, _, __)

    @action(detail=True, methods=('POST',), serializer_class=CreateSpymasterSerializer)
    def become_spymaster(self, request, *_, **__):
        return self.create(request, _, __)

    @action(detail=True, methods=('POST',))
    def start_game(self, request, *_, **__):
        game: Game = self.get_object()
        teams = TeamType.values
        if not (game.spymaster.filter(team__in=teams).count() == 2 and
                game.fieldoperative.filter(team__in=teams).count() >= 2):
            return Response({'detail': lz('Game can not be started, please unsure that each team has '
                                          '1 spymaster and at least 1 field operative')},
                            status=status.HTTP_400_BAD_REQUEST)
        game.status = GameStatus.STARTED
        game.last_turn = TeamType.RED
        game.save(update_fields=['status', 'last_turn'])

        game_cards = shuffled_game_cards(game)
        GameCard.objects.bulk_create(game_cards)

        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=('POST',))
    def play(self, request, *_, **__):
        game: Game = self.get_object()
        player, game_card_pk = request.user, request.data.get('game_card_pk', None)

        game_card = game.game_cards.filter(id=game_card_pk).first()
        if not game_card:
            return Response({'detail': lz('Wrong game card pk for the given game')},
                            status=status.HTTP_400_BAD_REQUEST)
        game_card_team = game_card.team
        if game_card.is_assassin:
            game_card.set_guessed()
            game.change_turn()
            game.set_status_finished()
        elif game_card_team is None:
            game_card.set_guessed()
            game.change_turn()
        elif game_card_team == game.last_turn:
            game_card.set_guessed()
            set_finished_if_winner(game, game_card_team)
        else:
            game_card.set_guessed()
            game.change_turn()
            set_finished_if_winner(game, game_card_team)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=('POST',))
    def end_turn(self, request, *_, **__):
        game: Game = self.get_object()
        game.change_turn()
        return Response(status=status.HTTP_200_OK)
