from django.urls import path, include
from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from authentication.views import RegisterViewSet

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('token/refresh/', refresh_jwt_token),
    path('token/verify/', verify_jwt_token,),
    path('register/', RegisterViewSet.as_view()),
]
