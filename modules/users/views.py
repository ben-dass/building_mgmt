import logging
from typing import Optional
from django.conf import settings
from djoser.social.views import ProviderAuthView
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

logger = logging.getLogger(__name__)


def set_auth_cookies(
    response: Response, access_token: str, refresh_token: Optional[str] = None
) -> Response:
    access_token_lifetime = settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()
    cookie_settings = {
        "path": settings.COOKIE_PATH,
        "secure": settings.COOKIE_SECURE,
        "httponly": settings.COOKIE_HTTPONLY,
        "samesite": settings.COOKIE_SAMESITE,
        "max_age": int(access_token_lifetime),
    }
    response.set_cookie("access", access_token, **cookie_settings)

    if refresh_token:
        refresh_token_lifetime = settings.SIMPLE_JWT[
            "REFRESH_TOKEN_LIFETIME"
        ].total_seconds()
        refresh_cookie_settings = cookie_settings.copy()
        refresh_cookie_settings["max_age"] = int(refresh_token_lifetime)
        response.set_cookie("refresh", refresh_token, **refresh_cookie_settings)

    logged_in_cookie_settings = cookie_settings.copy()
    logged_in_cookie_settings["httponly"] = False
    response.set_cookie("logged_in", "true", **logged_in_cookie_settings)


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        token_response = super().post(request, *args, **kwargs)

        if token_response.status_code == status.HTTP_200_OK:
            access_token = token_response.data.get("access")
            refresh_token = token_response.data.get("refresh")

            if access_token and refresh_token:
                set_auth_cookies(
                    token_response,
                    access_token=access_token,
                    refresh_token=refresh_token,
                )

                token_response.data.pop("access", None)
                token_response.data.pop("refresh", None)

                token_response.data["message"] = "Login successful."

            else:
                token_response.data["message"] = "Login failed."
                logger.error(
                    "Access token or refresh token not found in login response data."
                )

        return token_response


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        token_response = super().post(request, *args, **kwargs)

        if token_response.status_code == status.HTTP_200_OK:
            access_token = token_response.data.get("access")
            refresh_token = token_response.data.get("refresh")

            if access_token and refresh_token:
                set_auth_cookies(
                    token_response,
                    access_token=access_token,
                    refresh_token=refresh_token,
                )

                token_response.data.pop("access", None)
                token_response.data.pop("refresh", None)

                token_response.data["message"] = "Login successful."

            else:
                token_response.data["message"] = "Login failed."
                logger.error(
                    "Access token or refresh token not found in login response data."
                )

        return token_response
