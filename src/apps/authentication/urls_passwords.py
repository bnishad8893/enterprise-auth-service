"""URL routes for password management endpoints."""
from __future__ import annotations

from django.urls import path

from apps.authentication.views_passwords import (
    ChangePasswordAPIView,
    ForgotPasswordAPIView,
    ResetPasswordAPIView,
)

app_name = "authentication.passwords"

urlpatterns = [
    path("v1/auth/forgot-password/", ForgotPasswordAPIView.as_view(), name="forgot-password"),
    path("v1/auth/reset-password/", ResetPasswordAPIView.as_view(), name="reset-password"),
    path("v1/auth/change-password/", ChangePasswordAPIView.as_view(), name="change-password"),
]
