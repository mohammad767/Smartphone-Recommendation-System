from rest_framework import serializers
from apps.smartphones.serializers import BrandSerializer
from apps.smartphones.models import Brand
from .models import UserPreference





class UserPreferenceReadSerializer(serializers.ModelSerializer):

    preferred_brand = BrandSerializer()

    class Meta:
        model = UserPreference
        fields = [
            "user",
            "min_price",
            "max_price",
            "camera_weight",
            "battery_weight",
            "performance_weight",
            "display_weight",
            "preferred_brand",
            "created_at",
            "updated_at",
        ]


class UserPreferenceWriteSerializer(serializers.ModelSerializer):
    preferred_brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all(),required=False,allow_null=True,)
    class Meta:
        model = UserPreference
        fields = [
            "min_price",
            "max_price",
            "camera_weight",
            "battery_weight",
            "performance_weight",
            "display_weight",
            "preferred_brand",
        ]

    def validate_min_price(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                "Minimum price must be greater than 0."
            )

        return value

    def validate_max_price(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                "Maximum price must be greater than 0."
            )

        return value

    def validate(self, attrs):

        min_price = attrs.get(
            "min_price",
            getattr(self.instance, "min_price", None)
        )

        max_price = attrs.get(
            "max_price",
            getattr(self.instance, "max_price", None)
        )

        if (
            min_price is not None
            and max_price is not None
            and min_price > max_price
        ):
            raise serializers.ValidationError(
                "Minimum price cannot be greater than maximum price."
            )

        return attrs