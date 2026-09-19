from rest_framework import serializers
from .models import (
    Brand,
    Smartphone,
    SmartphoneSpecification,
    PriceHistory,
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
    smartphone = SmartPhoneReadSerializer()

    class Meta:
        model = SmartphoneSpecification
        fields = [
            "id",
            "ram",
            "storage",
            "battery",
            "camera",
            "display_type",
            "smartphone",
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
    # smartphone = SmartPhoneReadSerializer()

    class Meta:
        model = PriceHistory
        fields = [
            "id",
            # "smartphone",
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


    
class PhoneSpecificationReadSerializer(serializers.ModelSerializer):
    

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
    
    
    
    
class SmartphoneDetailSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    specification = PhoneSpecificationReadSerializer()

    latest_price = serializers.SerializerMethodField()
    class Meta:
        model = Smartphone
        fields = [
            "id",
            "name",
            "brand",
            "release_date",
            "specification",
            "latest_price",
            "created_at",
            "updated_at",
        ]
    def get_latest_price(self, obj):
        price = obj.price_history.first()

        if price:
            return price.price

        return None
    
    
    
    
