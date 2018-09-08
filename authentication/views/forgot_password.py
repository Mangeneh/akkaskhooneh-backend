from rest_framework import views, status, permissions
from rest_framework.response import Response

from authentication.models import User, Token

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth.password_validation import validate_password

import utils
import datetime


class ForgotPasswordApiView(views.APIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        if email is None:
            return Response(
                data={"details": "email is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user_query_set = User.objects.get(email=email)
        except ObjectDoesNotExist:
            return Response(
                data={"details": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        try:
            token = Token.objects.get(user=user_query_set)
            token.delete()
            token = Token.objects.create(user=user_query_set)
        except ObjectDoesNotExist:
            token = Token.objects.create(user=user_query_set)
        email = utils.send_email(
            to=email,
            subject="Token for forgot password",
            body="Your Token: {}".format(token.key)
        )
        if email.status_code == 200:
            return Response(
                data={"token": "ANANAS"},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                data={"details": "email api fail"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ForgotPasswordVerfication(views.APIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        token = request.data.get('token')
        if token is None:
            return Response(
                data={"details": "Token is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            token_query_set = Token.objects.get(key=token)
        except ObjectDoesNotExist:
            return Response(
                data={"details": "Token not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        token_time = int(token_query_set.created_time.strftime("%Y%m%d%H%M"))
        now_time = int(datetime.datetime.now().strftime("%Y%m%d%H%M"))
        ok_time = now_time - token_time  # One day = 10,000
        if ok_time <= 10000:
            return Response(
                data={"details": "Token is valid"},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                data={"details": "Token is invalid"},
                status=status.HTTP_401_UNAUTHORIZED
            )


class ForgotPasswordComplete(views.APIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request):

        token = request.data.get('token')
        password = request.data.get('password')
        if token is None or password is None:
            return Response(
                data={"details": "Token/Password is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            token_query_set = Token.objects.get(key=token)
        except ObjectDoesNotExist:
            return Response(
                data={"details": "Token not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        token_time = int(token_query_set.created_time.strftime("%Y%m%d%H%M"))
        now_time = int(datetime.datetime.now().strftime("%Y%m%d%H%M"))
        ok_time = now_time - token_time  # One day = 10,000
        if ok_time <= 10000:
            try:
                validate_password(password)
            except ValidationError:
                return Response(
                    data={"details": "Password is not valid."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user_query_set = User.objects.get(user=token_query_set.user)
            user_query_set.set_password(password)
            user_query_set.save()
            return Response(
                data={"details": "Password Changed."},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                data={"details": "Token is invalid"},
                status=status.HTTP_401_UNAUTHORIZED
            )
