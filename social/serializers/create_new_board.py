from rest_framework.serializers import ModelSerializer
from social.models import Board


class CreateNeqBoardSerializer(ModelSerializer):

    class Meta:
        model = Board
        fields = ('owner', 'name')