from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from social.models import Posts


class CreateNewPostAPIView(APIView):

    def post(self, request, format=None):
        user = request.user
        picture = request.FILES.get('picture')
        caption = request.POST.copy().get('caption')

        if user is None:
            res = {'details': 'user is not authorized'}
            return Response(res, status.HTTP_400_BAD_REQUEST)
        if picture is None:
            res = {'details': 'picture not found'}
            return Response(res, status.HTTP_400_BAD_REQUEST)

        post = Posts.objects.create(owner=user, picture=picture, caption=caption)
        post.save()
        res = {'details': 'created successfully'}
        return Response(res, status.HTTP_201_CREATED)
