from rest_framework import serializers

from .models import (
    Brand,
    Chipset,
    Smartphone,
    PriceHistory
)



# =====================
# Brand
# =====================

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



# =====================
# Chipset
# =====================


class ChipsetSerializer(serializers.ModelSerializer):

    class Meta:

        model = Chipset

        fields = [
            "id",
            "name",
            "antutu_score",
            "geekbench_multi",
        ]



class ChipsetWriteSerializer(serializers.ModelSerializer):

    class Meta:

        model = Chipset

        fields = [
            "name",
            "antutu_score",
            "geekbench_multi",
        ]



# =====================
# Smartphone Read
# =====================


class SmartphoneReadSerializer(serializers.ModelSerializer):

    brand = BrandSerializer()

    chipset = ChipsetSerializer()


    class Meta:

        model = Smartphone

        fields = [
            "id",
            "name",
            "brand",
            "release_date",

            "chipset",

            "ram_gb",
            "storage_gb",
            "storage_type",

            "battery_mah",
            "fast_charging_w",

            "display_refresh_hz",
            "display_ppi",

            "main_camera_mp",
            "has_ois",

            "created_at",
            "updated_at",
        ]



# =====================
# Smartphone Write
# =====================


class SmartphoneWriteSerializer(serializers.ModelSerializer):

    brand = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.all()
    )


    chipset = serializers.PrimaryKeyRelatedField(
        queryset=Chipset.objects.all()
    )


    class Meta:

        model = Smartphone

        fields = [

            "name",
            "brand",
            "release_date",

            "chipset",

            "ram_gb",
            "storage_gb",
            "storage_type",

            "battery_mah",
            "fast_charging_w",

            "display_refresh_hz",
            "display_ppi",

            "main_camera_mp",
            "has_ois",

        ]


    def validate_name(self,value):

        if not value.strip():
            raise serializers.ValidationError(
                "Name cannot be empty."
            )

        return value



    def validate_ram_gb(self,value):

        if value <=0:
            raise serializers.ValidationError(
                "RAM must be positive."
            )

        return value



    def validate_storage_gb(self,value):

        if value <=0:
            raise serializers.ValidationError(
                "Storage must be positive."
            )

        return value



    def validate_battery_mah(self,value):

        if value <=0:
            raise serializers.ValidationError(
                "Battery must be positive."
            )

        return value



    def validate_main_camera_mp(self,value):

        if value <=0:
            raise serializers.ValidationError(
                "Camera must be positive."
            )

        return value



# =====================
# Price History
# =====================


class PriceHistoryReadSerializer(serializers.ModelSerializer):

    class Meta:

        model = PriceHistory

        fields = [
            "id",
            "price",
            "created_at",
        ]



class PriceHistoryWriteSerializer(serializers.ModelSerializer):

    smartphone = serializers.PrimaryKeyRelatedField(
        queryset=Smartphone.objects.all()
    )


    class Meta:

        model = PriceHistory

        fields = [
            "smartphone",
            "price",
        ]



    def validate_price(self,value):

        if value <=0:

            raise serializers.ValidationError(
                "Price must be greater than zero."
            )

        return value



# =====================
# Smartphone Detail
# =====================


class SmartphoneDetailSerializer(serializers.ModelSerializer):

    brand = BrandSerializer()

    chipset = ChipsetSerializer()


    latest_price = serializers.SerializerMethodField()


    price_history = PriceHistoryReadSerializer(
        many=True
    )


    class Meta:

        model = Smartphone

        fields = [

            "id",
            "name",

            "brand",

            "release_date",

            "chipset",

            "ram_gb",
            "storage_gb",
            "storage_type",

            "battery_mah",
            "fast_charging_w",

            "display_refresh_hz",
            "display_ppi",

            "main_camera_mp",
            "has_ois",

            "latest_price",
            "price_history",

            "created_at",
            "updated_at",

        ]



    def get_latest_price(self,obj):

        price = obj.price_history.first()

        if price:
            return price.price

        return None