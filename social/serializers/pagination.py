from rest_framework.serializers import ModelSerializer
from social.models.posts import Posts


class PaginationSerializer(ModelSerializer):
    class Meta:
        model = Posts
        fields = ('id', 'picture',)
