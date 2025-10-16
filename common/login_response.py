from rest_framework_simplejwt.tokens import RefreshToken


def user_login_token_response(user, club_id=None):
    """
    Returns a standardized user + JWT token dict
    """
    refresh = RefreshToken.for_user(user)

    response = {
        "user": {
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        },
        "token": {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        },
    }

    if club_id is not None:
        response["club_id"] = club_id

    return response
