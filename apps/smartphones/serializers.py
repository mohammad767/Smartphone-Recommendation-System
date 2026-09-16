from rest_framework import serializers

from .models import (
    Brand,
    Smartphone,
    SmartphoneSpecification,
    PriceHistory,
    UserPreference,
)


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = [
            "id",
            "name",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class SmartPhoneReadSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()

    class Meta:
        model = Smartphone
        fields = [
            "id",
            "name",
            "brand",
            "release_date",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class SmartPhoneWriteSerializer(serializers.ModelSerializer):
    brand = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.all()
    )

    class Meta:
        model = Smartphone
        fields = [
            "id",
            "name",
            "brand",
            "release_date",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Name cannot be empty."
            )

        if len(value) > 200:
            raise serializers.ValidationError(
                "Name is too long."
            )

        return value


class SpecificationReadSerializer(serializers.ModelSerializer):
    # smartphone = SmartPhoneReadSerializer()

    class Meta:
        model = SmartphoneSpecification
        fields = [
            "id",
            "ram",
            "storage",
            "battery",
            "camera",
            "display_type",
            "processor",
            "weight",
        ]


class SpecificationWriteSerializer(serializers.ModelSerializer):
    smartphone = serializers.PrimaryKeyRelatedField(
        queryset=Smartphone.objects.all()
    )

    class Meta:
        model = SmartphoneSpecification
        fields = [
            "id",
            "smartphone",
            "ram",
            "storage",
            "battery",
            "camera",
            "display_type",
            "processor",
            "weight",
        ]
        read_only_fields = [
            "id",
        ]

    def validate_smartphone(self, value):
        if hasattr(value, "specification"):
            raise serializers.ValidationError(
                "This smartphone already has a specification."
            )

        return value

    def validate_ram(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "RAM must be greater than 0."
            )

        if value > 64:
            raise serializers.ValidationError(
                "RAM value is too high."
            )

        return value

    def validate_storage(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Storage must be greater than 0."
            )

        if value > 2048:
            raise serializers.ValidationError(
                "Storage value is too high."
            )

        return value

    def validate_battery(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Battery must be greater than 0."
            )

        if value > 20000:
            raise serializers.ValidationError(
                "Battery value is too high."
            )

        return value

    def validate_camera(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Camera must be greater than 0."
            )

        if value > 500:
            raise serializers.ValidationError(
                "Camera value is too high."
            )

        return value

    def validate_processor(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Processor cannot be empty."
            )

        return value

    def validate_weight(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Weight must be greater than 0."
            )

        if value > 1000:
            raise serializers.ValidationError(
                "Weight value is too high."
            )

        return value


class PriceHistoryReadSerializer(serializers.ModelSerializer):
    smartphone = SmartPhoneReadSerializer()

    class Meta:
        model = PriceHistory
        fields = [
            "id",
            "smartphone",
            "price",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
        ]


class PriceHistoryWriteSerializer(serializers.ModelSerializer):
    smartphone = serializers.PrimaryKeyRelatedField(
        queryset=Smartphone.objects.all()
    )

    class Meta:
        model = PriceHistory
        fields = [
            "id",
            "smartphone",
            "price",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
        ]

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Price must be greater than 0."
            )

        return value


class UserPreferenceReadSerializer(serializers.ModelSerializer):
    preferred_brand = BrandSerializer()

    class Meta:
        model = UserPreference
        fields = [
            "id",
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
    preferred_brand = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.all()
    )

    class Meta:
        model = UserPreference
        fields = [
            "id",
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
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        min_price = attrs.get("min_price")
        max_price = attrs.get("max_price")

        if min_price is not None and max_price is not None:
            if min_price > max_price:
                raise serializers.ValidationError(
                    "Minimum price is bigger than maximum price."
                )

        if not all(
            0 <= value <= 100
            for value in (
                attrs["camera_weight"],
                attrs["battery_weight"],
                attrs["performance_weight"],
                attrs["display_weight"],
            )
        ):
            raise serializers.ValidationError(
                "Weight must be between 0 and 100."
            )

        return attrs

    def validate_user(self, value):
        if hasattr(value, "preference"):
            raise serializers.ValidationError(
                "This user already has a preference."
            )

        return value
    
    
class SmartphoneDetailSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    specification = SpecificationReadSerializer()

    class Meta:
        model = Smartphone
        fields = [
            "id",
            "name",
            "brand",
            "release_date",
            "specification",
            "created_at",
            "updated_at",
        ]