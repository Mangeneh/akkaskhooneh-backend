from rest_framework import views, status
from rest_framework.response import Response
from django.db.models import Count
from social.models import Tags, TagContains
import utils
from settings.base import MEDIA_URL


class TopHashtagListApiView(views.APIView):

    def get(self, request, format=None):
        Tags_query_set = TagContains.objects.values('tag_id').annotate(
            count=Count('tag')).order_by('-count')
        page_number = request.data.get('page')
        pages = utils.paginator(Tags_query_set, page=page_number)
        results = pages.get('result')
        count = pages.get('count')
        total_page = pages.get('total_page')
        results_list = []
        url = str(request.scheme) + '://' + request.get_host() + MEDIA_URL
        for item in results:
            tag_query_set = Tags.objects.get(id=item['tag_id'])
            tag_id = tag_query_set.id
            tag_name = tag_query_set.name
            picture = url + str(TagContains.objects.filter(
                tag=tag_query_set).order_by('-id')[0].post.picture)
            new_item = {
                "tag_id": tag_id,
                "tag_name": tag_name,
                "picture": picture
                }
            results_list.append(new_item)
        data = {
            "total_pages": total_page,
            "count": count,
            "results": results_list
        }

        return Response(data=data , status=status.HTTP_200_OK)