from rest_framework import views, status
from rest_framework.response import Response
from authentication.models import User
from social.models import Request, Followers
from django.core.exceptions import ObjectDoesNotExist


class FollowRequest(views.APIView):

    def post(self, request):
        target_user_name = request.data.get('username')
        if target_user_name is None:
            return Response(
                data={"error": "Username required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            target_user_query_set = User.objects.get(username=target_user_name)
        except ObjectDoesNotExist:
            return Response(
                data={"error": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        if target_user_query_set.is_private:
            try:
                follow_status = Followers.objects.get(
                    user=request.user,
                    following=target_user_query_set
                )
                return Response(
                    data={"error": "You are already followed this user"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except ObjectDoesNotExist:
                request_object, create = Request.objects.get_or_create(
                    requester=request.user,
                    requestee=target_user_query_set
                )
                if create:
                    return Response(
                        data={"detail": "Follow request created."},
                        status=status.HTTP_201_CREATED
                    )
                else:
                    return Response(
                        data={
                            "details": "You are already requested fore follow this user."
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
        else:
            try:
                follow_status = Followers.objects.get(
                    user=request.user,
                    following=target_user_query_set
                )
                return Response(
                    data={"error": "You are already followed this user"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except ObjectDoesNotExist:
                follow_create = Followers(
                    user=request.user,
                    following=target_user_query_set
                )
                follow_create.save()
                return Response(
                    data={"details": "You are successfully follow this user."},
                    status=status.HTTP_200_OK
                )
