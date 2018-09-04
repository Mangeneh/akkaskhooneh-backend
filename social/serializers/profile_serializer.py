from rest_framework import serializers
from authentication.models import User
from social.models.followers import Followers


class ProfileSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()

    followers = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username',
                  'fullname', 'bio', 'following', 'followers', 'email', 'profile_picture')

    def get_followers(self, obj):
        followers = Followers.objects.filter(following=obj.id).count()
        return followers

    def get_following(self, obj):
        following = Followers.objects.filter(user=obj.id).count()
        return following
