from django.urls import path, include
from django.conf.urls import url
from authentication import views
from rest_framework_simplejwt.views import (
    token_obtain_pair,
    token_verify,
    token_refresh
)

urlpatterns = [
    path('register/', views.RegisterViewSet.as_view()),
    path('changepassword/', views.ChangePassword.as_view()),
    path('login/', token_obtain_pair, name='token_obtain_pair'),
    path('token/refresh/', token_refresh, name='token_refresh'),
    path('token/verify/', token_verify, name='token_verify'),
]
