from django.urls import path, include

from social.views.profile_view_set import ProfileViewSet
from social.views.set_profile_view_set import SetProfilePicViewSet

urlpatterns = [
    path('profile/<str:username>', ProfileViewSet.as_view()),
    path('profile/', ProfileViewSet.as_view()),
    path('change-pic/', SetProfilePicViewSet.as_view())
]
