from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import exceptions
from .models import UserPreference
from .serializers import UserPreferenceReadSerializer,UserPreferenceWriteSerializer
from rest_framework.generics import get_object_or_404

from rest_framework.permissions import IsAuthenticated


class UserPreferenceAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request) : 
        preference = get_object_or_404(UserPreference,user=request.user)
        serializer = UserPreferenceReadSerializer(preference)
        return Response({"data" : serializer.data},status=status.HTTP_200_OK)
    
    def post(self, request):
        user = request.user
        serializer = UserPreferenceWriteSerializer(data=request.data)
        if serializer.is_valid():
            preference = serializer.save(user=user)
            read_serializer = UserPreferenceReadSerializer(preference)
            return Response({"data": read_serializer.data}, status=status.HTTP_200_OK)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    
    def patch(self,request) : 
        user = request.user
        preference = get_object_or_404(UserPreference,user=request.user)
        serializer = UserPreferenceWriteSerializer(preference,data=request.data,partial=True)
        if serializer.is_valid() : 
            new_preferenc =serializer.save()
            read_serializer = UserPreferenceReadSerializer(new_preferenc)
            return Response({"data" : read_serializer.data},status=status.HTTP_200_OK)
        return Response({"errors" : serializer.errors},status=status.HTTP_400_BAD_REQUEST)