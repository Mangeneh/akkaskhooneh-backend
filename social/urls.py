from django.urls import path, include

from social.views.create_new_post_api_view import CreateNewPostAPIView
from social.views.profile_view_set import ProfileViewSet
from social.views.set_profile_view_set import SetProfilePicViewSet
from social.views.pagination import PaginationApiView
from social.views.user_boards_api_view import UserBoardsApiView

urlpatterns = [
    path('profile/<str:username>', ProfileViewSet.as_view()),
    path('profile/', ProfileViewSet.as_view()),
    path('change-pic/', SetProfilePicViewSet.as_view()),
    path('pictures/', PaginationApiView.as_view()),
    path('pictures/<str:username>', PaginationApiView.as_view()),
    path('create-new-post/', CreateNewPostAPIView.as_view()),
    path('boards/', UserBoardsApiView.as_view()),
    path('boards/<str:username>/', UserBoardsApiView.as_view())
]
