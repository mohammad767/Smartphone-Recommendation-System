from django.urls import path
from .views import (RequestOTPAPIView,VerifyOTPAPIView,
                    ProfileAPIView,)

from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns =[
    path("request-otp/",RequestOTPAPIView.as_view()),
    path("verify-otp/",VerifyOTPAPIView.as_view()),
    path("profile/",ProfileAPIView.as_view()),
    path("token/refresh/",TokenRefreshView.as_view()),
]