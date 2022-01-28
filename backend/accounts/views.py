from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.serializers import CreateUserSerializer


class CreateUserView(CreateAPIView):
    queryset = get_user_model()
    serializer_class = CreateUserSerializer
    permission_classes = [~IsAuthenticated]


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_logout(request):
    token = RefreshToken(request.data.get('refresh'))
    token.blacklist()
    return Response("Success", status=status.HTTP_205_RESET_CONTENT)
