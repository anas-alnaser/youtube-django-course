from django.shortcuts import get_object_or_404
from api.serializers import OrderSerializer, ProductInfoSerializer, ProductSerializer
from api.models import Order, Product, User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Max


#views.py file
@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


#views.py file
@api_view(['GET'])
def order_list(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


# @api_view(['GET'])
# def user_list(request):
#     user = User.objects.all()
#     serializer = UserSerializer(user, many=True)
#     return Response(serializer.data)


@api_view(['GET'])
def product_info(request):
    products = Product.objects.all()
    serializer = ProductInfoSerializer({
        'products':
        products,
        'count':
        len(products),
        'max_price':
        products.aggregate(max_price=Max('price'))['max_price']
    })
    return Response(serializer.data)
