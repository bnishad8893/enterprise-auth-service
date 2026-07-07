"""URL configuration for the authentication app."""
from __future__ import annotations

from django.urls import path

from apps.authentication.views import (
    LoginAPIView,
    LogoutAPIView,
    TokenRefreshAPIView,
    TokenVerifyAPIView,
)

app_name = "authentication"

urlpatterns = [
    path("v1/auth/login/", LoginAPIView.as_view(), name="login"),
    path("v1/auth/refresh/", TokenRefreshAPIView.as_view(), name="refresh"),
    path("v1/auth/verify/", TokenVerifyAPIView.as_view(), name="verify"),
    path("v1/auth/logout/", LogoutAPIView.as_view(), name="logout"),
]
