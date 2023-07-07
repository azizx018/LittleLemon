from django.contrib.auth.models import User
from rest_framework import serializers

from LittleLemonAPI.models import Cart, Cateogry, MenuItem, Order, OrderItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Cateogry
        fields = ['id','slug','title']

class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = MenuItem
        fields = ['id','title','price', 'featured', 'category', 'category_id']


class CartSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)
    price = serializers.SerializerMethodField(method_name= 'calculate_price')
    class Meta:
        model = Cart
        fields = ['id','user','menuitem', 'quantity', 'unit_price', 'price', 'menuitem_id', 'user_id']

    def calculate_price(self, product:Cart):
        return product.unit_price * product.quantity    


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id','status','total', 'date', 'delivery_crew_id','user_id']

class OrderItemSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = OrderItem
        fields = ['id','quantity', 'unit_price', 'price', 'menuitem_id', 'order_id']     

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'






# class MenuItemSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)
#     price = serializers.DecimalField(max_digits=6, decimal_places=2)
#     featured = serializers.BooleanField()