from django.urls import path
from .views import CalculateScore,RecommendationAPIView


urlpatterns = [
    # path("calc-score/",CalculateScore.as_view()),
    path("",RecommendationAPIView.as_view())
]
