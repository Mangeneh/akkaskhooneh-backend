from django.urls import path, include

from social.views import AddNewPostToBoard, FeedAPI
from social.views import BoardDetailsAPI
from social.views import CreateNewPostAPIView
from social.views import ProfileViewSet
from social.views import SetProfilePicViewSet
from social.views import PaginationApiView
from social.views import CreateNewBoardApiView
from social.views import UserBoardsApiView
from social.views import DeletePostFromBoard
from social.views import DeleteBoard
from social.views import PostDetailApiView
from social.views import UserSearchApiView
from social.views import TagSearchApiView

urlpatterns = [
    path('profile/<str:username>/', ProfileViewSet.as_view()),
    path('profile/', ProfileViewSet.as_view()),
    path('change-pic/', SetProfilePicViewSet.as_view()),
    path('pictures/', PaginationApiView.as_view()),
    path('pictures/<str:username>/', PaginationApiView.as_view()),
    path('create-new-post/', CreateNewPostAPIView.as_view()),
    path('boardsdetails/<int:board_id>/', BoardDetailsAPI.as_view()),
    path('create-new-board/', CreateNewBoardApiView.as_view()),
    path('boards/', UserBoardsApiView.as_view()),
    path('boards/<str:username>/', UserBoardsApiView.as_view()),
    path('addnewposttoboard/', AddNewPostToBoard.as_view()),
    path('deletepostfromboard/', DeletePostFromBoard.as_view()),
    path('deleteboard/', DeleteBoard.as_view()),
    path('post/<int:id>/', PostDetailApiView.as_view()),
    path('usersearch/', UserSearchApiView.as_view()),
    path('feed/', FeedAPI.as_view()),
    path('tagsearch/', TagSearchApiView.as_view()),
]
