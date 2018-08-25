from rest_framework import generics, pagination
from rest_framework.response import Response

from social.models.posts import Posts
from authentication.models.user import User
from social.serializers.pagination import PaginationSerializer


class StandardPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PaginationApiView(generics.ListAPIView):
    """ This api view use for make pagination for pictures in user account"""
    queryset = Posts.objects.all()
    serializer_class = PaginationSerializer
    pagination_class = StandardPagination

    def get(self, request, username=None, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        update = {'owner': request.user}
        if username:
            update.update({'owner': User.objects.get(username=username)})

        queryset = queryset.filter(**update)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
