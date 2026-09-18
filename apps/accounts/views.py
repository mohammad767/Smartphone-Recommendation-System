from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import exceptions
from .serializers import (
    RequestOTPSerializer,
    VerifyOTPSerializer,
    UserReadSerializer,
    UserUpdateSerializer,
)

from rest_framework.permissions import IsAuthenticated
from .services.otp import create_otp_session, verify_otp

from django.shortcuts import get_object_or_404

from rest_framework_simplejwt.tokens import RefreshToken


class RequestOTPAPIView(APIView):
    def post(self, request):
        serializer = RequestOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        otp_data = create_otp_session(user)
        return Response(
            {"otp": otp_data["otp"], "temp_token": otp_data["temp_token"]},
            status=status.HTTP_200_OK,
        )


class VerifyOTPAPIView(APIView):

    def post(self, request):

        serializer = VerifyOTPSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )


        user = verify_otp(
            serializer.validated_data["temp_token"],
            serializer.validated_data["otp"]
        )


        if not user:
            return Response(
                {
                    "error": "Invalid OTP"
                },
                status=status.HTTP_400_BAD_REQUEST
            )


        refresh = RefreshToken.for_user(user)


        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": UserReadSerializer(user).data
            },
            status=status.HTTP_200_OK
        )
        
class ProfileAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def get(self, request):

        user = request.user
        serializer = UserReadSerializer(user)
        return Response({"data" : serializer.data},status=status.HTTP_200_OK)
    
    def patch(self,request) : 
        user = request.user
        serializer = UserUpdateSerializer(user,data=request.data,pratial=True)
        if serializer.is_valid() : 
            user = serializer.save()
            read_serializer = UserReadSerializer(user)
            return Response({"data" : read_serializer.data},status=status.HTTP_200_OK)
        return Response({"errors" : serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        