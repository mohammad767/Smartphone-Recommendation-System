from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import exceptions
from .models import Brand,Smartphone,PriceHistory
from .serializers import (BrandSerializer,SmartphoneReadSerializer,
                            SmartphoneWriteSerializer,SmartphoneDetailSerializer,
                          PriceHistoryReadSerializer,PriceHistoryWriteSerializer,
                          )
from rest_framework.generics import get_object_or_404

from rest_framework.permissions import IsAuthenticated


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
        phones = phones = Smartphone.objects.select_related("brand","chipset")
        serializer = SmartphoneReadSerializer(phones,many=True)
        return Response({"data" : serializer.data},status=status.HTTP_200_OK)
    
    def post(self,request) : 
        serializer = SmartphoneWriteSerializer(data=request.data)
        if serializer.is_valid() :
            phone = serializer.save()
            read_serializer = SmartphoneWriteSerializer(phone)
            return Response({"data" : read_serializer.data},status=status.HTTP_201_CREATED)
        return Response({"errors" : serializer.errors},status.HTTP_400_BAD_REQUEST)
    
class SmartphoneDetailAPIView(APIView) : 
    def get(self,request,pk) : 
        phone = get_object_or_404(Smartphone.objects.select_related("brand","chipset").prefetch_related("price_history"),pk=pk)
        
        serializer = SmartphoneDetailSerializer(phone)
        return Response({"data" : serializer.data},status=status.HTTP_200_OK)
    
    def patch(self,request,pk) : 
        phone = get_object_or_404(Smartphone, pk=pk)
        serializer = SmartphoneWriteSerializer(phone,data=request.data,partial=True)
        if serializer.is_valid() : 
            phone = serializer.save()
            read_serializer = SmartphoneReadSerializer(phone)
            return Response({"data" : read_serializer.data},status=status.HTTP_200_OK)
        
        return Response({"errors" : serializer.errors},status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk) : 
        phone = get_object_or_404(Smartphone, pk=pk)
        phone.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
        

    

class PriceHistoryAPIView(APIView) :
    def get(self,request,pk) :
        prices = PriceHistory.objects.filter(smartphone_id=pk).order_by("-created_at")
        serializer = PriceHistoryReadSerializer(prices,many=True)
        return Response({"data" : serializer.data},status=status.HTTP_200_OK)
        
    def post(self,request,pk) :
        data = request.data.copy()
        smartphone = get_object_or_404(Smartphone,pk=pk)
        data["smartphone"] = smartphone.id
        
        serializer = PriceHistoryWriteSerializer(data=data)
        if serializer.is_valid() : 
            price = serializer.save()

            read_serializer = PriceHistoryReadSerializer(price)

            return Response({"data": read_serializer.data},status=status.HTTP_201_CREATED)
        
        return Response({"errors" : serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    

class PriceHistoryDetailAPIView(APIView):

    def delete(self, request, pk):

        price = get_object_or_404(
            PriceHistory,
            pk=pk
        )

        price.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
        
        
