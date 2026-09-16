from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import exceptions
from .models import Brand,Smartphone
from .serializers import BrandSerializer,SmartPhoneReadSerializer,SmartPhoneWriteSerializer,SmartphoneDetailSerializer
from rest_framework.generics import get_object_or_404


class BrandAPIView(APIView):
    def get(self, request):
        brands = Brand.objects.all().order_by("id")
        serializer = BrandSerializer(brands,many=True)
        
        return Response({"data" : serializer.data},status=status.HTTP_200_OK)
        
    def post(self,request) : 
        serializer = BrandSerializer(data=request.data)
        if serializer.is_valid() :
            serializer.save()
            return Response({"data" : serializer.data},status=status.HTTP_201_CREATED)
        
        return Response({"message" : serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
class BrandDetailAPIView(APIView) :

    def get(self,request,pk) : 
        brand = get_object_or_404(Brand, pk=pk)
        serializer = BrandSerializer(brand)
        return Response({"data" : serializer.data},status=status.HTTP_200_OK)
    
    def patch(self,request,pk) : 
        brand = get_object_or_404(Brand, pk=pk)
        serializer = BrandSerializer(brand,data=request.data,partial=True)
        if serializer.is_valid() :
            serializer.save()
            return Response(
                {"data": serializer.data},
                status=status.HTTP_200_OK
            )
        
        return Response({"errors" : serializer.errors},status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk) : 
        brand = get_object_or_404(Brand, pk=pk)
        brand.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
        
        
class SmartphoneAPIView(APIView) :
    def get(self,request) : 
        phones = Smartphone.objects.select_related("brand").order_by("created_at")
        serializer = SmartPhoneReadSerializer(phones,many=True)
        return Response({"data" : serializer.data},status=status.HTTP_200_OK)
    
    def post(self,request) : 
        serializer = SmartPhoneWriteSerializer(data=request.data)
        if serializer.is_valid() :
            phone = serializer.save()
            read_serializer = SmartPhoneReadSerializer(phone)
            return Response({"data" : read_serializer.data},status=status.HTTP_201_CREATED)
        return Response({"errors" : serializer.errors},status.HTTP_400_BAD_REQUEST)
    
class SmartphoneDetailAPIView(APIView) : 
    def get(self,request,pk) : 
        phone = get_object_or_404(Smartphone.objects.select_related("brand").prefetch_related("specification"),pk=pk)
        
        serializer = SmartphoneDetailSerializer(phone)
        return Response({"data" : serializer.data},status=status.HTTP_200_OK)
    
    def patch(self,request,pk) : 
        phone = get_object_or_404(Smartphone, pk=pk)
        serializer = SmartPhoneWriteSerializer(phone,data=request.data,partial=True)
        if serializer.is_valid() : 
            phone = serializer.save()
            read_serializer = SmartPhoneReadSerializer(phone)
            return Response({"data" : read_serializer.data},status=status.HTTP_200_OK)
        
        return Response({"errors" : serializer.errors},status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk) : 
        phone = get_object_or_404(Smartphone, pk=pk)
        phone.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        