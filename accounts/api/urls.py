from django.contrib import admin
from django.conf import settings
from django.urls import path,include
from django.conf.urls.static import static
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token
from .views import RegisterUserView,PasswordTokenCheckAPI,RequestPasswordResetEmail,SetNewPasswordAPIView,UserList


urlpatterns = [
    path('register/', RegisterUserView.as_view()),
    path('users/', UserList.as_view()),
    path('login/', obtain_jwt_token),
    path('token-auth-refresh/', refresh_jwt_token),
    path('token-auth-verify/', verify_jwt_token),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(), name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name="password-reset-confirm"),
    path('password-reset-complete/', SetNewPasswordAPIView.as_view(),
         name='password-reset-complete')
]