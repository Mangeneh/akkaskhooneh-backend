import json
from authentication.models import User


def create_user(data):
    parsed_data = json.loads(data)

    username = parsed_data.get("username")
    password = parsed_data.get("password")
    email = parsed_data.get("email")
    fullname = parsed_data.get("fullname")
    bio = parsed_data.get("bio")
    phone_number = parsed_data.get("phone_number")
    profile_picture = None
    # TODO profile picture

    if username is None or \
            password is None or \
            email is None:
        return None

    user = User.objects.create(username=username, password="", email=email)

    user.set_password(password)

    if fullname is not None:
        user.fullname = fullname

    if bio is not None:
        user.bio = bio

    if phone_number is not None:
        user.phone_number = phone_number

    if profile_picture is not None:
        user.profile_picture = profile_picture

    user.save()

    return user
