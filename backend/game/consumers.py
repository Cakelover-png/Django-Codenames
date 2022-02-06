import json
import random

from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as lz
from djangochannelsrestframework.decorators import action
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.mixins import RetrieveModelMixin
from djangochannelsrestframework.observer import model_observer
from djangochannelsrestframework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import ValidationError

from game.choices import TeamType, GameStatus
from game.models import Game, Spymaster, FieldOperative, Card, GameCard
from game.serializers import RetrieveGameSerializer
from game.utils.custom_functions import set_finished_if_winner


class GameConsumer(RetrieveModelMixin,
                   GenericAsyncAPIConsumer):
    queryset = Game.objects.select_related('creator').prefetch_related('fieldoperative__player',
                                                                       'spymaster__player',
                                                                       'game_cards__card')
    serializer_class = RetrieveGameSerializer
    permission_classes = [IsAuthenticated]

    async def connect(self):
        self.group_name = 'game_' + str(
            (dict((x.split('=') for x in self.scope['query_string'].decode().split("&")))).get('pk'))
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    @action()
    async def join_game(self, pk, **kwargs):
        game: Game = await database_sync_to_async(self.get_object)(pk=pk)
        await self.add_user_to_game_lobby(game)
        return {}, status.HTTP_200_OK

    @action()
    async def leave_game(self, pk, **kwargs):
        game: Game = await database_sync_to_async(self.get_object)(pk=pk)
        await self.remove_user_from_game_lobby(game)
        return {}, status.HTTP_200_OK

    @action()
    async def become_spymaster(self, pk, team, **kwargs):
        game: Game = await database_sync_to_async(self.get_object)(pk=pk)
        player = self.scope['user']
        await self.delete_spymaster_and_field_operative(game, player)
        await database_sync_to_async(Spymaster.objects.create)(game_id=game.id, player_id=player.id, team=team)
        return {}, status.HTTP_200_OK

    @action()
    async def become_field_operative(self, pk, team, **kwargs):
        game: Game = await database_sync_to_async(self.get_object)(pk=pk)
        player = self.scope['user']
        await self.delete_spymaster_and_field_operative(game, player)
        await database_sync_to_async(FieldOperative.objects.create)(game_id=game.id, player_id=player.id, team=team)
        return {}, status.HTTP_200_OK

    @action()
    async def start_game(self, pk, **kwargs):
        game: Game = await database_sync_to_async(self.get_object)(pk=pk)
        await self.set_status_and_turn(game)
        await self.shuffle_and_create_game_cards(game)
        return {}, status.HTTP_200_OK

    @action()
    async def play(self, pk, game_card_pk, **kwargs):
        game: Game = await database_sync_to_async(self.get_object)(pk=pk)
        await self.check_and_modify_game_state(game, game_card_pk)
        return {}, status.HTTP_200_OK

    @action()
    async def end_turn(self, pk, **kwargs):
        game: Game = await database_sync_to_async(self.get_object)(pk=pk)
        await database_sync_to_async(game.change_turn)()
        return {}, status.HTTP_200_OK

    @action()
    async def notify_users(self, pk, **kwargs):
        game: Game = await database_sync_to_async(self.get_object)(pk=pk)
        await self.notify_users_about_game(game)
        return {}, status.HTTP_200_OK

    async def notify_users_about_game(self, game):
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'update_game',
                'data': await self.get_game_data(game)
            }
        )

    async def update_game(self, event: dict):
        await self.send(text_data=json.dumps({'data': event['data'], 'action': 'notify_users'}))

    @database_sync_to_async
    def get_game_data(self, game: Game):
        return RetrieveGameSerializer(game, context=self.get_serializer_context()).data

    @database_sync_to_async
    def remove_user_from_game_lobby(self, game: Game):
        user: User = self.scope['user']
        game.players_in_lobby.remove(user)

    @database_sync_to_async
    def add_user_to_game_lobby(self, game: Game):
        user: User = self.scope['user']
        if not game.players_in_lobby.filter(id=user.id).exists():
            game.players_in_lobby.add(user)

    @database_sync_to_async
    def delete_spymaster_and_field_operative(self, game: Game, player: User):
        Spymaster.objects.filter(game_id=game.id, player_id=player.id).delete()
        FieldOperative.objects.filter(game_id=game.id, player_id=player.id).delete()

    @database_sync_to_async
    def shuffle_and_create_game_cards(self, game: Game):
        if GameCard.objects.filter(game_id=game.id).count() == 0:
            cards = random.sample(list(Card.objects.all().values_list('id', flat=True)), 25)
            game_cards = [GameCard(game_id=game.id, card_id=cards[i], team=TeamType.RED) for i in range(9)]
            game_cards.extend([GameCard(game_id=game.id, card_id=cards[i], team=TeamType.BLUE) for i in range(9, 17)])
            game_cards.extend([GameCard(game_id=game.id, card_id=cards[i]) for i in range(17, 24)])
            game_cards.extend([GameCard(game_id=game.id, card_id=cards[24], is_assassin=True)])
            random.shuffle(game_cards)
            GameCard.objects.bulk_create(game_cards)

    @database_sync_to_async
    def set_status_and_turn(self, game: Game):
        game.status = GameStatus.STARTED
        game.last_turn = TeamType.RED
        game.save(update_fields=['status', 'last_turn'])

    @database_sync_to_async
    def check_and_modify_game_state(self, game: Game, game_card_pk: int):
        game_card = game.game_cards.filter(id=game_card_pk).first()
        if not game_card:
            raise ValidationError({'detail': lz('Wrong game card pk for the given game')})
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
        return {}, status.HTTP_200_OK
