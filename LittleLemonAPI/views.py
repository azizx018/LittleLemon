
from unicodedata import name
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from .models import Cart, MenuItem, Order, OrderItem
from .models import Cateogry
from .serializers import CartSerializer, CategorySerializer, MenuItemSerializer, OrderSerializer, UserSerializer, OrderItemSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token
import datetime

from LittleLemonAPI import serializers

# Create your views here.
# @permission_classes([IsAuthenticated])
# class MenuItemView(generics.ListCreateAPIView):
#     if generics.RetrieveAPIView:
#         queryset = MenuItem.objects.all()
#         serializer_class = MenuItemSerializer

class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer   
      
class OrderItemView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderItemSerializer 
    
class CategoryView(generics.ListCreateAPIView):
        queryset = Cateogry.objects.all()
        serializer_class = CategorySerializer 

class CartView(generics.ListCreateAPIView):
        queryset = Cart.objects.all()
        serializer_class = CartSerializer               
   

@api_view(['GET','POST'])
def menu_items(request):
    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all()
        serialized_item = MenuItemSerializer(items, many=True)
        return Response(serialized_item.data)
    
    if request.method == 'POST' and request.user.groups.filter(name='Manager'):
        serialized_item = MenuItemSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status.HTTP_201_CREATED)
    else:
        return Response({"message":"You are not authorized"}, 403)    


@api_view(['GET', 'DELETE', 'PUT','PATCH'])
def single_item(request, id):
    if request.method == 'GET':
        item = get_object_or_404(MenuItem, pk=id)
        serialized_item = MenuItemSerializer(item)
        return Response(serialized_item.data, status=status.HTTP_200_OK)
    if request.method == 'DELETE' and request.user.groups.filter(name='Manager'):
        item = MenuItem.objects.filter(id=id)
        item.delete()
        return Response({"message":"Menu item has been deleted"}, status.HTTP_200_OK)

    if request.method == 'PUT' or 'PATCH' and request.user.groups.filter(name='Manager'):
        item = MenuItem.objects.filter(id=id).first()
        serialized_item = MenuItemSerializer(item, data=request.data, partial=True)
        if serialized_item.is_valid():
            serialized_item.save()
            return Response({"message":"Item has been updated"}, status=status.HTTP_200_OK)    

    return Response({"message":"You are  not authorized"}, 403)
         


@api_view()
def single_order(request,id):
    order = get_object_or_404(Order, pk=id)
    serialized_item = OrderSerializer(order)
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
   

@api_view(['POST','DELETE', 'GET'])
@permission_classes([IsAuthenticated])
def managers(request):
    if request.method == 'GET':
        users = User.objects.filter(groups__name='Manager')
        user_serializer = UserSerializer(users, many=True)
        return Response({"data": user_serializer.data}, 200)
    username = request.data['username']
    if username:
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name="Manager")
            
        if request.method == 'POST':        
            managers.user_set.add(user)
            return Response({"message":"User added to manager group"}, 201)
        elif request.method == 'DELETE':
            managers.user_set.remove(user)    
        return Response({"message":"User deleted from manager group"}, 200)

    return Response({"message": "error"}, status.HTTP_400_BAD_REQUEST)   

@api_view(['POST','DELETE', 'GET'])
@permission_classes([IsAuthenticated])
def delivery(request):
    if request.method == 'GET':
        users = User.objects.filter(groups__name='Delivery crew')
        user_serializer = UserSerializer(users, many=True)
        return Response({"data": user_serializer.data}, 200)
    username = request.data['username']
    if username:
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name="Delivery crew")
            
        if request.method == 'POST':        
            managers.user_set.add(user)
            return Response({"message":"User added to delivery group"}, 201)
        elif request.method == 'DELETE':
            managers.user_set.remove(user)    
        return Response({"message":"User deleted from delivery group"}, 200)

    return Response({"message": "error"}, status.HTTP_400_BAD_REQUEST)   

@api_view(['GET', 'POST','DELETE'])
@permission_classes([IsAuthenticated])
def cart(request):
    username = request.data['username']
    user_id = Token.objects.get(key=request.auth.key).user_id
    if request.method == 'GET' and username:
        cart = Cart.objects.all()
        serialized_cart = CartSerializer(cart, many=True)
        return Response({"data":serialized_cart.data}, 200)
    
    if request.method == 'POST' and username:
        serialized_cart = CartSerializer(data=request.data)
        serialized_cart.is_valid(raise_exception=True)
        serialized_cart.save()
        return Response(serialized_cart.data, status.HTTP_201_CREATED)  
    if request.method == 'DELETE' and username:
        cart = Cart.objects.all()
        cart.delete()
        return Response({"message":"Menu item has been deleted"}, status.HTTP_200_OK)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def order(request):
    username = request.data['username']
    user_id = Token.objects.get(key=request.auth.key).user_id
    user = User.objects.get(id=user_id)
    
    ## gets current user order if username is present
    if request.method == 'GET' and username:
        order = Order.objects.all()
        serialized_order = OrderSerializer(order, many=True)
        return Response({"data":serialized_order.data}, 200)
       
    if request.method == 'POST' and username:
        current_user = request.user
        # serialized_order = Order.objects.create(user_id=current_user.id)
        # serialized_order.save()
        serialized_order = OrderSerializer(data=request.data)
        serialized_order.is_valid(raise_exception=True)
        # validatedData = serialized_order.validated_data
        # user_id = validatedData.get('id')
        
        serialized_order.save(user_id = user)
        return Response(serialized_order.data, status.HTTP_201_CREATED)
        # else:
            # return Response(serialized_order.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # cart = Cart.objects.all()
        # serialized_order_item = OrderItemSerializer(data=request.data)
        # serialized_order_item.is_valid()
        # serialized_order_item.save(cart)
        # cart.delete()
        

@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name='Manager').exists():
        return Response({"message":"Only manager should see this."})
    else:
        return Response({"message":"You are NOT authorized"}, 403)    

@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
    return Response({"message":"successful"})

@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def throttle_check_auth(request):
    return Response({"message":"message for logged in users only"})      