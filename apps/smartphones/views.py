from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import exceptions
from .models import Brand,Smartphone,SmartphoneSpecification,PriceHistory,UserPreference
from .serializers import (BrandSerializer,SmartPhoneReadSerializer,
                          SmartPhoneWriteSerializer,SmartphoneDetailSerializer,
                          SpecificationWriteSerializer,SpecificationReadSerializer,
                          PriceHistoryReadSerializer,PriceHistoryWriteSerializer,
                          UserPreferenceReadSerializer,UserPreferenceWriteSerializer)
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
        phone = get_object_or_404(Smartphone.objects.select_related("brand","specification").prefetch_related("price_history"),pk=pk)
        
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
        
        
class SpecificationAPIView(APIView):

    def post(self, request, pk):

        smartphone = get_object_or_404(Smartphone,pk=pk)

        data = request.data.copy()
        data["smartphone"] = smartphone.id

        serializer = SpecificationWriteSerializer(data=data)

        if serializer.is_valid():

            specification = serializer.save()

            read_serializer = SpecificationReadSerializer(specification)

            return Response({"data": read_serializer.data},status=status.HTTP_201_CREATED)

        return Response({"errors": serializer.errors},status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request, pk):

        specification = get_object_or_404(SmartphoneSpecification,smartphone_id=pk)

        serializer = SpecificationWriteSerializer(specification,data=request.data,partial=True)

        if serializer.is_valid():

            specification = serializer.save()

            read_serializer = SpecificationReadSerializer(specification)

            return Response({"data": read_serializer.data},status=status.HTTP_200_OK)

        return Response({"errors": serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):

        specification = get_object_or_404(SmartphoneSpecification,smartphone_id=pk)

        specification.delete()

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