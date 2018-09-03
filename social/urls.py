from django.urls import path, include

from social.views.add_new_post_to_board import AddNewPostToBoard
from social.views.board_datails_view import BoardDetailsAPI
from social.views.create_new_post_api_view import CreateNewPostAPIView
from social.views.profile_view_set import ProfileViewSet
from social.views.set_profile_view_set import SetProfilePicViewSet
from social.views.pagination import PaginationApiView
from social.views.create_board_apiview import CreateNewBoardApiView
from social.views.user_boards_api_view import UserBoardsApiView

urlpatterns = [
    path('profile/<str:username>/', ProfileViewSet.as_view()),
    path('profile/', ProfileViewSet.as_view()),
    path('change-pic/', SetProfilePicViewSet.as_view()),
    path('pictures/', PaginationApiView.as_view()),
    path('pictures/<str:username>/', PaginationApiView.as_view()),
    path('create-new-post/', CreateNewPostAPIView.as_view()),
    path('boardsdatails/<int:board_id>/', BoardDetailsAPI.as_view()),
    path('create-new-board/', CreateNewBoardApiView.as_view()),
    path('boards/', UserBoardsApiView.as_view()),
    path('boards/<str:username>/', UserBoardsApiView.as_view()),
    path('addnewposttoboard/', AddNewPostToBoard.as_view()),
]
