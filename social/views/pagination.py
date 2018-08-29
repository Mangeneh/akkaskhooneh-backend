from rest_framework import generics, pagination, status
from rest_framework.response import Response

from social.models.posts import Posts
from authentication.models.user import User
from social.serializers.pagination import PaginationSerializer
from django.core.exceptions import ObjectDoesNotExist


class StandardPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PaginationApiView(generics.ListAPIView):
    """ This api view use for make pagination for pictures in user account"""
    queryset = Posts.objects.all().order_by('-time')
    serializer_class = PaginationSerializer
    pagination_class = StandardPagination

    def get(self, request, username=None, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        update = {'owner': request.user}
        if username:
            try:
                us = User.objects.get(username=username)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            update.update({'owner': us})

        queryset = queryset.filter(**update)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
