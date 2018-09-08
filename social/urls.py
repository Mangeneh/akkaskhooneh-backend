from django.urls import path, include

from social.views import *

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
    path('search/user/', UserSearchApiView.as_view()),
    path('feed/', FeedAPI.as_view()),
    path('search/tags/', TagSearchApiView.as_view()),
    path('search/followers/<str:username>/', FollowerSearchApiView().as_view()),
    path('search/following/<str:username>/', FollowingSearchApiView().as_view()),
    path('followers/<str:username>/', FollowerSearchApiView().as_view()),
    path('following/<str:username>/', FollowingSearchApiView().as_view()),
    path('tophashtag/', TopHashtagListApiView.as_view()),
    path('request/', FollowRequest.as_view()),
    path('tag/<int:tag_id>/', GetPostOfTagAPI.as_view()),
    path('request/accept/', AcceptFollowRequestAPIView.as_view()),
    path('followrequest/', GetFollowReqAPI.as_view()),
    path('like/', LikeAPI.as_view()),
    path('comment/', CommentAPIView.as_view()),
]
