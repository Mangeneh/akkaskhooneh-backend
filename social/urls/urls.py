from django.urls import path, include

from social.views.profile_view_set import ProfileViewSet

urlpatterns = [
    path('profile/<str:username>', ProfileViewSet.as_view()),
    path('profile/', ProfileViewSet.as_view()),
]
