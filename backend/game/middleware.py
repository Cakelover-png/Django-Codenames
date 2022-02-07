import os

import django
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser, User
from django.db import close_old_connections
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken

from game.utils.custom_functions import get_query_params

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_codenames.settings')
django.setup()


@database_sync_to_async
def get_user(access_token):
    try:
        validated_token = AccessToken(access_token)
    except TokenError:
        return AnonymousUser()
    try:
        user_id = validated_token['user_id']
    except KeyError:
        return AnonymousUser()
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()

    if not user.is_active:
        return AnonymousUser()

    return user


class TokenAuthMiddleware(BaseMiddleware):

    async def __call__(self, scope, receive, send):
        close_old_connections()
        try:
            access_token = get_query_params(scope['query_string']).get('access_token')
        except ValueError:
            access_token = None
        scope['user'] = await get_user(access_token)
        return await super().__call__(scope, receive, send)


def JWTAuthMiddlewareStack(inner):
    return TokenAuthMiddleware(inner)
