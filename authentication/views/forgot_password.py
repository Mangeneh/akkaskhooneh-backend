from rest_framework import views, status, permissions
from rest_framework.response import Response

from authentication.models import User, Token

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth.password_validation import validate_password

import utils
import datetime
import logging

logger = logging.getLogger('authentication')


class ForgotPasswordApiView(views.APIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request):

        ip = utils.get_client_ip(request)

        utils.start_method_log(
            'ForgotPasswordApiView: post', ip=ip)

        email = request.data.get('email')
        if email is None:
            logger.info(
                'ForgotPasswordApiView: '
                'post (Email is required. ip: {})'.format(ip))
            return Response(
                data={"details": "email is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user_query_set = User.objects.get(email=email)
        except ObjectDoesNotExist:
            logger.info(
                'ForgotPasswordApiView: '
                'post (User not found. ip: {})'.format(ip))
            return Response(
                data={"details": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        try:
            token = Token.objects.get(user=user_query_set)

            token_time = token.created_time
            now_time = datetime.datetime.now(datetime.timezone.utc)
            ok_time = now_time - token_time
            if ok_time.seconds > 300:
                token.delete()
                token = Token.objects.create(user=user_query_set)
            else:
                logger.info(
                    'ForgotPasswordApiView: '
                    'post (Try again later for create token. ip: {})'.format(ip))
                return Response(
                    data={"details": "Please try again a few minutes later"},
                    status=status.HTTP_403_FORBIDDEN
                )
        except ObjectDoesNotExist:
            token = Token.objects.create(user=user_query_set)
        email = utils.send_email(
            to=email,
            subject="Token for forgot password",
            body="Your Token: {}".format(token.key)
        )
        if email.status_code == 200:
            logger.info(
                'ForgotPasswordApiView: post (Ok , Token send to this '
                'email:{email} ip: {ip})'.format(ip=ip, email=email))
            return Response(
                data={},
                status=status.HTTP_201_CREATED
            )
        else:
            logger.info(
                'ForgotPasswordApiView: post '
                '(Email API fail. ip: {})'.format(ip))
            return Response(
                data={"details": "email api fail"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ForgotPasswordVerfication(views.APIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request):

        ip = utils.get_client_ip(request)

        utils.start_method_log(
            'ForgotPasswordVerfication: post', ip=ip)

        token = request.data.get('token')
        if token is None:
            logger.info(
                'ForgotPasswordVerfication: '
                'post (Token is required. ip: {})'.format(ip))
            return Response(
                data={"details": "Token is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            token_query_set = Token.objects.get(key=token)
        except ObjectDoesNotExist:
            logger.info(
                'ForgotPasswordVerfication: '
                'post (Token not found. ip: {})'.format(ip))
            return Response(
                data={"details": "Token not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        token_time = int(token_query_set.created_time.strftime("%Y%m%d%H%M"))
        now_time = int(datetime.datetime.now().strftime("%Y%m%d%H%M"))
        ok_time = now_time - token_time  # One day = 10,000
        if ok_time <= 10000:
            logger.info(
                'ForgotPasswordVerfication: '
                'post (Token is valid. ip: {})'.format(ip))
            return Response(
                data={"details": "Token is valid"},
                status=status.HTTP_200_OK
            )
        else:
            token_query_set.delete()
            logger.info(
                'ForgotPasswordVerfication: post '
                '(Token is invalid. ip: {})'.format(ip))
            return Response(
                data={"details": "Token is invalid"},
                status=status.HTTP_401_UNAUTHORIZED
            )


class ForgotPasswordComplete(views.APIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request):

        ip = utils.get_client_ip(request)

        utils.start_method_log(
            'ForgotPasswordComplete: post', ip=ip)

        token = request.data.get('token')
        password = request.data.get('password')
        if token is None or password is None:
            logger.info(
                'ForgotPasswordComplete: post '
                '(Token/Password is required. ip: {})'.format(ip))
            return Response(
                data={"details": "Token/Password is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            token_query_set = Token.objects.get(key=token)
        except ObjectDoesNotExist:
            logger.info(
                'ForgotPasswordComplete: post '
                '(Token not found. ip: {})'.format(ip))
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
                logger.info(
                    'ForgotPasswordComplete: post '
                    '(Password is not valid. ip: {})'.format(ip))
                return Response(
                    data={"details": "Password is not valid."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user_query_set = User.objects.get(user=token_query_set.user)
            user_query_set.set_password(password)
            user_query_set.save()
            token_query_set.delete()
            logger.info(
                'ForgotPasswordComplete: post '
                '(Password successfully changed. '
                'email: {email} ip: {ip})'.format(
                    ip=ip, email=user_query_set.email))
            return Response(
                data={"details": "Password Changed."},
                status=status.HTTP_200_OK
            )
        else:
            logger.info(
                'ForgotPasswordComplete: post '
                '(Token is invalid. ip: {})'.format(ip))
            return Response(
                data={"details": "Token is invalid"},
                status=status.HTTP_401_UNAUTHORIZED
            )
