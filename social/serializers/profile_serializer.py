from enum import Enum

from rest_framework import serializers
from authentication.models import User
from social.models.followers import Followers, Request


class ProfileSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    following_status = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username',
                  'fullname', 'bio', 'following', 'followers', 'email', 'profile_picture', 'following_status', 'is_private')

    def get_followers(self, obj):
        followers = Followers.objects.filter(following=obj.id).count()
        return followers

    def get_following(self, obj):
        following = Followers.objects.filter(user=obj.id).count()
        return following

    def get_following_status(self, user):
        requset_user = self.context.get('request_user')

        if Followers.objects.filter(user=requset_user, following=user).count():
            return FollowingType.Following.value
        if Request.objects.filter(requester=requset_user, requestee=user).count():
            return FollowingType.Requested.value
        return FollowingType.NotFollowing.value

class FollowingType(Enum):
    Following = 1
    Requested = 2
    NotFollowing = 3