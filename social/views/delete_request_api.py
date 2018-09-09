from rest_framework import views, status
from rest_framework.response import Response
from authentication.models import User
from social.models import Request, Followers
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError


class DeleteFollowRequest(views.APIView):

    def post(self, request):
        target_user_name = request.data.get('username')

        if target_user_name is None:
            return Response(
                data={"error": "Username required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            target_user = User.objects.get(username=target_user_name)
        except ObjectDoesNotExist:
            return Response(
                data={"error": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            request = Request.objects.get(requester=request.user, requestee=target_user)
        except ObjectDoesNotExist:
            return Response(
                data={"error": "You didnt request this user."},
                status=status.HTTP_404_NOT_FOUND
            )

        request.delete()
        return Response(data={'details':'Follow request deleted succesfully'}, status=status.HTTP_200_OK)