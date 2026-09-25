from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.pagination import PageNumberPagination

from apps.smartphones.models import Smartphone
from .serializers import RecommendationSerializer
from .engine import get_recommendations
from .scoring import calculate_and_save_scores_bulk


class RecommendationPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class CalculateScore(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request):
        phones = list(Smartphone.objects.select_related("chipset").all())
        calculate_and_save_scores_bulk(phones)
        return Response(
            {"message": f"Scores recalculated for {len(phones)} phones"},
            status=status.HTTP_200_OK,
        )


class RecommendationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        recommendations = get_recommendations(request.user)

        paginator = RecommendationPagination()
        page = paginator.paginate_queryset(recommendations, request, view=self)
        serializer = RecommendationSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)