from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import exceptions
from .models import Brand
from .serializers import BrandSerializer
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
        
        
        