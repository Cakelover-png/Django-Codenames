from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.serializers import CreateUserSerializer, UserSerializer


class CreateUserView(CreateAPIView):
    queryset = get_user_model()
    serializer_class = CreateUserSerializer
    permission_classes = [~IsAuthenticated]


class GetUserDataView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        serializer = UserSerializer(User.objects.get(id=request.user.id))
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_logout(request):
    token = RefreshToken(request.data.get('refresh'))
    token.blacklist()
    return Response("Success", status=status.HTTP_205_RESET_CONTENT)
