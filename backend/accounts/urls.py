from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.views import user_logout, CreateUserView, GetUserDataView

app_name = 'accounts'

urlpatterns = [
    path('register/', CreateUserView.as_view()),
    path('userdata/', GetUserDataView.as_view(), name='userdata'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', user_logout)
]
