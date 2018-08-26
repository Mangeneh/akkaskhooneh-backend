from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import User
from authentication.serializers import EmailSerializer


class CheckEmailApiView(APIView):
    """ This api view use for check email address exist in database."""

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            email = request.POST.get('email')
            try:
                User.objects.get(email=email)
            except ObjectDoesNotExist:
                return Response({
                    "message": "Email does not exist."
                }, status=status.HTTP_200_OK)
            return Response({
                "message": "Email exists"
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "message": "Email address is not valid"
            }, status=status.HTTP_400_BAD_REQUEST)
