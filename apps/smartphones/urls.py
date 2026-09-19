from django.urls import path
from .views import (BrandAPIView, BrandDetailAPIView,
                    SmartphoneAPIView,SmartphoneDetailAPIView,
                    SpecificationAPIView,PriceHistoryAPIView,PriceHistoryDetailAPIView,
                    UserPreferenceAPIView
                    )

urlpatterns = [
    path("brands/",BrandAPIView.as_view()),
    path("brands/<int:pk>/",BrandDetailAPIView.as_view()),
    path("smartphones/",SmartphoneAPIView.as_view()),
    path("smartphones/<int:pk>/",SmartphoneDetailAPIView.as_view()),
    path("smartphones/<int:pk>/specification/",SpecificationAPIView.as_view()),
    path("smartphones/<int:pk>/prices/",PriceHistoryAPIView.as_view()),
    path("prices/<int:pk>/",PriceHistoryDetailAPIView.as_view()),
    
    # path("smartphones/<int:pk>/specification/edit/",SpecificationDetailAPIView.as_view()),
    
            
]