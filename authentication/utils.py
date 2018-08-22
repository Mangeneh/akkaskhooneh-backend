from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.six import text_type

def get_simplejwt_tokens(user):
    """This foucntion get a User object and return 'access' and 'refresh' tokens."""

    tokens = RefreshToken.for_user(user)
    refresh = text_type(tokens)
    access = text_type(tokens.access_token)
    data = {
        "refresh": refresh,
        "access": access
    }

    return data
