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


# Set auth related cookies on the response object.
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


# Customizes the TokenObtainPairView:
#   If access & refresh tokens are valid, store them in auth cookies and remove them from response.
class CustomTokenObtainPairView(TokenObtainPairView):
    # Overriding the POST method from TokenObtainPairView.
    # This method is called when a user submits login credentials.
    def post(self, request: Request, *args, **kwargs) -> Response:

        #  Calls the original TokenObtainPairView.post method that:
        #  - Validates user credentials.
        #  - Generates new access & refresh tokens.
        #  - Returns a JSON reponse like:
        #   {
        #       "access": "ACCESS_TOKEN",
        #       "refresh": "REFRESH_TOKEN"
        #   }
        token_response = super().post(request, *args, **kwargs)

        # If the login is successful.
        if token_response.status_code == status.HTTP_200_OK:
            access_token = token_response.data.get("access")
            refresh_token = token_response.data.get("refresh")

            if access_token and refresh_token:
                set_auth_cookies(
                    token_response,
                    access_token=access_token,
                    refresh_token=refresh_token,
                )

                #  Remove the tokens from the JSON response to prevent localStorage storing.
                token_response.data.pop("access", None)
                token_response.data.pop("refresh", None)

                token_response.data["message"] = "Login successful."

            else:
                token_response.data["message"] = "Login failed."
                logger.error(
                    "Access token or refresh token not found in login response data."
                )

        return token_response


# Customizes the TokenRefreshView:
#   Securely refresh JWT access tokens by reading the refresh token from auth cookies.
class CustomTokenRefreshView(TokenRefreshView):
    # Overriding the POST method from TokenRefreshView.
    # This method is called when:
    #   - Access token has expired.
    #   - Automatic refresh of the access token.
    #   - Manual refresh of the access token.
    def post(self, request: Request, *args, **kwargs) -> Response:

        # Instead of getting the refresh token from frontend logic, get it from the cookie.
        refresh_token = request.COOKIES.get("refresh")
        if refresh_token:
            request.data["refresh"] = refresh_token

        #  Calls the original TokenRefreshView.post method that:
        #  - Validates the refresh token.
        #  - Refreshes the access token.
        #  - Returns a JSON reponse like:
        #   {
        #       "access": "NEW_ACCESS_TOKEN",
        #       "refresh": "NEW_REFRESH_TOKEN"
        #   }
        refresh_response = super().post(request, *args, **kwargs)

        # Check to see if token refresh was successful.
        if refresh_response.status_code == status.HTTP_200_OK:
            access_token = refresh_response.data.get("access")
            refresh_token = refresh_response.data.get("refresh")

            # Store new tokens in cookies.
            if access_token and refresh_token:
                set_auth_cookies(
                    refresh_response,
                    access_token=access_token,
                    refresh_token=refresh_token,
                )

                #  Remove the tokens from the JSON response to prevent localStorage storing.
                refresh_response.data.pop("access", None)
                refresh_response.data.pop("refresh", None)

                refresh_response.data["message"] = (
                    "Access token refreshed successfully."
                )

            else:
                refresh_response.data["message"] = (
                    "Access or refresh token not found in refresh response data."
                )
                logger.error(
                    "Access token or refresh token not found in refresh response data."
                )

        return refresh_response


# When a user logs in via Google, the authentication process follows these steps:
# 1. Frontend sends the Google OAuth token here (via POST) after user logs in with their Google account.
# 2. The backend (ProviderAuthView.post) validates the OAuth token using the following:
#    - SOCIAL_AUTH_GOOGLE_OATH2_KEY
#    - SOCIAL_AUTH_GOOGLE_OATH2_SECRET
# 3. Once token is validated, it retrieves the user's information from Google (email, name, etc.) and creates/updates a user in the Django database.
# 4. The backend will then generate an access and refresh token, storing them in secure cookies.
class CustomProviderAuthView(ProviderAuthView):

    def post(self, request: Request, *args, **kwargs) -> Response:

        #  Calls the original ProviderAuthView.post method that:
        #  - Gets the OAuth token from the Frontend.
        #  - Validates the Google OAuth token.
        #  - Retrieve user information from Google.
        #  - Creates/updates a user in the Django database.
        #  - Generates access & refresh tokens.
        provider_response = super().post(request, *args, **kwargs)

        # If the login is successful.
        if provider_response.status_code == status.HTTP_201_CREATED:
            access_token = provider_response.data.get("access")
            refresh_token = provider_response.data.get("refresh")

            if access_token and refresh_token:
                set_auth_cookies(
                    provider_response,
                    access_token=access_token,
                    refresh_token=refresh_token,
                )

                #  Remove the tokens from the JSON response to prevent localStorage storing.
                provider_response.data.pop("access", None)
                provider_response.data.pop("refresh", None)

                provider_response.data["message"] = "Login successful."

            else:
                provider_response.data["message"] = (
                    "Access or refresh token not found in provider response."
                )
                logger.error(
                    "Access token or refresh token not found in provider response data."
                )

        return provider_response


class LogoutView(APIView):
    def post(self, request: Request, *args, **kwargs):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        response.delete_cookie("logged_in")
        response.data = {"message": "Logout successful."}
        return response
