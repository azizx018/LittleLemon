from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import MenuItem
from .models import Cateogry
from .serializers import CategorySerializer, MenuItemSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import generics

# Create your views here.
class MenuItemView(generics.ListCreateAPIView):
    
        queryset = MenuItem.objects.all()
        serializer_class = MenuItemSerializer

class CategoryView(generics.ListCreateAPIView):
    
        queryset = Cateogry.objects.all()
        serializer_class = CategorySerializer        
   



@api_view(['GET', 'POST'])
def menu_items(request):
    if request.method == 'GET':
        items = MenuItem.objects.all()
        serialized_item = MenuItemSerializer(items, many=True)
        return Response(serialized_item.data)
    if request.method == 'POST':
       serialized_item = MenuItemSerializer(data=request.data)
       serialized_item.is_valid(raise_exception=True)
       serialized_item.save()
       return Response(serialized_item.data, status.HTTP_201_CREATED)

@api_view()
def single_item(request,id):
    item = get_object_or_404(MenuItem, pk=id)
    serialized_item = MenuItemSerializer(item)
    return Response(serialized_item.data)

@api_view(['GET','POST'])
def category(request):
    if request.method == 'GET':
        category = Cateogry.objects.all()
        serialized_category = CategorySerializer(category, many=True)
        return Response(serialized_category.data)
    if request.method == 'POST':
        serialized_category = CategorySerializer(data=request.data)
        serialized_category.is_valid(raise_exception=True)
        serialized_category.save()    
        return Response(serialized_category.data, status.HTTP_201_CREATED)

@api_view()
def secret(request):
    return Response({"message":"Some secret message"})          
