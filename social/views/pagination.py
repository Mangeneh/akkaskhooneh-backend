from rest_framework import generics, pagination
from social.models.posts import Posts
from authentication.models.user import User
from social.serializers.pagination import PaginationSerializer

class StandardPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PaginationApiView(generics.ListAPIView):
  """ This api view use for make pagination for pictures in user account"""

  serializer_class = PaginationSerializer
  pagination_class = StandardPagination

  def get_queryset(self):
    if self.us is None:
      user = self.request.user
    else:
      user = self.us
    return Posts.objects.filter(owner=user)

  def get(self, request, username=None, *args, **kwargs):
        if username:
          self.us = User.objects.get(username=username).id
        else:
          self.us = None
        return self.list(request, *args, **kwargs)
