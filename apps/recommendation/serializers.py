from rest_framework import serializers
from apps.smartphones.serializers import SmartphoneReadSerializer


class RecommendationSerializer(serializers.Serializer):
    smartphone = SmartphoneReadSerializer()
    latest_price = serializers.IntegerField()
    recommendation_score = serializers.FloatField(source="score")
    breakdown = serializers.DictField()