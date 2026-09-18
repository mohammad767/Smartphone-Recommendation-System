from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import (
    OTPSession,
    PHONE_VALIDATOR,
)


User = get_user_model()


class RequestOTPSerializer(serializers.Serializer):

    phone = serializers.CharField(
        max_length=13
    )


    def validate_phone(self, value):

        PHONE_VALIDATOR(value)

        # normalize phone number
        if value.startswith("+98"):
            value = "0" + value[3:]

        return value


    def validate(self, attrs):

        phone = attrs["phone"]

        user, created = User.objects.get_or_create(
            phone=phone
        )

        attrs["user"] = user

        return attrs



class VerifyOTPSerializer(serializers.Serializer):

    temp_token = serializers.UUIDField()

    otp = serializers.CharField(
        max_length=6,
        min_length=6
    )


    def validate_temp_token(self, value):

        if not OTPSession.objects.filter(
            temp_token=value
        ).exists():

            raise serializers.ValidationError(
                "Invalid temp token."
            )

        return value


    def validate_otp(self, value):

        if not value.isdigit():

            raise serializers.ValidationError(
                "OTP must contain only numbers."
            )

        return value



class UserReadSerializer(serializers.ModelSerializer):

    class Meta:

        model = User

        fields = [
            "id",
            "full_name",
            "phone",
            "email",
            "birth_date",
            "profile_img",
            "is_active",
            "is_staff",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "phone",
            "is_active",
            "is_staff",
            "created_at",
            "updated_at",
        ]



class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:

        model = User

        fields = [
            "full_name",
            "email",
            "birth_date",
            "profile_img",
        ]

        read_only_fields = [
            "phone",
        ]


    def validate_email(self, value):

        if value == "":
            return None

        return value