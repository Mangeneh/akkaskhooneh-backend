from functools import reduce

from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from operator import or_

import utils
from social.models import Tags
from social.serializers.tag_search_serializer import TagSearchSerializer
from settings.base import MEDIA_URL
import difflib


class TagSearchApiView(APIView):

    def get(self, request, format=None):
        ip = utils.get_client_ip(request)

        utils.start_method_log('TagSearchApiView: get',
                               username=request.user.username, ip=ip)

        page = request.GET.get('page')
        search_value = request.GET.get('search')

        if search_value is None:
            return Response({'datails': 'search value required'}, status=status.HTTP_400_BAD_REQUEST)

        search_array = search_value.split(' ')

        data = Tags.objects.filter(reduce(or_, [Q(name__icontains=q) for q in search_array])).order_by('-id')

        data = list(data).copy()
        data.sort(key=lambda obj: sum([difflib.SequenceMatcher(None, obj.name, q).ratio()
                                       for q in search_array]), reverse=True)

        url = str(request.scheme) + '://' + request.get_host() + MEDIA_URL
        serializer = TagSearchSerializer(self.request.user, context={'page': page, 'url': url, 'data': data,
                                                                     'request_user': self.request.user})
        return Response(serializer.data)
