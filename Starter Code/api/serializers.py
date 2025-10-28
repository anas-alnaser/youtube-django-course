from rest_framework import serializers
from rest_framework import serializers

from .models import *

#serializer.py file

# class UserSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = User
#         fields = ('id', 'username', 'is_staff')


class ProductSerializer(serializers.ModelSerializer):
    """The product serializer to convert he python command to json file and vice verca"""

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'stock')

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be grater than 0")

        return value


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    product_price = serializers.DecimalField(source='product.price',
                                             max_digits=10,
                                             decimal_places=2)

    class Meta:
        model = OrderItem
        fields = ('product_name', 'product_price', 'quantity', 'item_subtotal')


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    # user_info = UserSerializer(source='user', many=False, read_only=True)

    def get_total_price(self, obj):
        order_items = obj.items.all()
        return sum(order_items.item_subtotal for order_items in order_items)

    class Meta:
        model = Order
        fields = ('order_id', 'created_at', 'user', 'status', 'items',
                  'total_price')


#we expant by Seializer class no modelserializer
class ProductInfoSerializer(serializers.Serializer):
    #get all product , count of product , max price
    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()
