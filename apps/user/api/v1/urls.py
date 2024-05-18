from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.user.api.v1.views import LoginView, RegisterView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login_get_token_view'),
    path('login/refresh/', TokenRefreshView.as_view(), name='login_refresh_token_view'),
    path('register/', RegisterView.as_view(), name='registration'),
]
