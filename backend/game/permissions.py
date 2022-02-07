from typing import Dict, Any

from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from djangochannelsrestframework.permissions import BasePermission

from game.choices import GameStatus
from game.models import Game
from game.utils.custom_functions import get_query_params


class IsInLobby(BasePermission):
    async def has_permission(self, scope: Dict[str, Any], consumer: AsyncConsumer, action: str, **kwargs) -> bool:
        if action in ('retrieve', 'become_spymaster', 'become_field_operative',
                      'start_game', 'play', 'end_turn'):
            pk = get_query_params(scope['query_string']).get('pk')
            user = scope.get('user')
            return await self.check_if_in_lobby(pk, user)
        return True

    @database_sync_to_async
    def check_if_in_lobby(self, pk, user):
        return Game.objects.filter(pk=pk, players_in_lobby=user).exists()


class CanStartGame(BasePermission):
    async def has_permission(self, scope: Dict[str, Any], consumer: AsyncConsumer, action: str, **kwargs) -> bool:
        if action == 'start_game':
            pk = get_query_params(scope['query_string']).get('pk')
            user = scope.get('user')
            return await self.check_if_creator(pk, user)
        return True

    @database_sync_to_async
    def check_if_creator(self, pk, user):
        return Game.objects.filter(pk=pk, creator=user).exists()


class HasStatusPending(BasePermission):
    async def has_permission(self, scope: Dict[str, Any], consumer: AsyncConsumer, action: str, **kwargs) -> bool:
        if action in ('become_spymaster', 'become_field_operative', 'start_game'):
            pk = get_query_params(scope['query_string']).get('pk')
            return await self.check_status(pk)
        return True

    @database_sync_to_async
    def check_status(self, pk):
        return Game.objects.filter(pk=pk, status=GameStatus.PENDING).exists()


class HasStatusStarted(BasePermission):
    async def has_permission(self, scope: Dict[str, Any], consumer: AsyncConsumer, action: str, **kwargs) -> bool:
        if action in ('play', 'end_turn'):
            pk = get_query_params(scope['query_string']).get('pk')
            return await self.check_status(pk)
        return True

    @database_sync_to_async
    def check_status(self, pk):
        return Game.objects.filter(pk=pk, status=GameStatus.STARTED).exists()
