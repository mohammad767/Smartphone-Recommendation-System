from django.urls import path
from .views import BrandAPIView, BrandDetailAPIView

urlpatterns = [
    path("brands/",BrandAPIView.as_view()),
    path("brands/<int:pk>/",BrandDetailAPIView.as_view()),
    
            
]