from django.shortcuts import get_object_or_404
from api.serializers import OrderSerializer, ProductInfoSerializer, ProductSerializer
from api.models import Order, Product, User
from rest_framework.response import Response
from django.db.models import Max
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView

# --- "GENERIC" CLASS-BASED VIEWS (The easy way) ---
# These are pre-built views from DRF that handle common patterns.


class OrderListAPIView(generics.ListAPIView):
    """
    Handles GET requests to '/orders/' (example path)
    'ListAPIView' provides *only* a 'GET' method to list all items.
    """
    # 'queryset' is the main data for this view.
    # '.prefetch_related()' is a *critical performance optimization*.
    # It tells Django: "When you get all the Orders, go ahead and
    # also fetch all their related 'items' and those items' 'products'
    # in a few big, efficient queries."
    # This prevents the "N+1 query problem" where you would otherwise
    # run a new query for *every single item in every single order*.
    queryset = Order.objects.prefetch_related('items__product')

    # Tell the view which serializer to use for translation.
    serializer_class = OrderSerializer


class UserOrderListAPIView(generics.ListAPIView):
    """
    Handles GET requests to '/my-orders/' (example path)
    This is just like OrderListAPIView, but with two key differences.
    """
    # We start with the same optimized queryset
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer

    # 1. PERMISSION: This line *locks* the view.
    # Only users who are logged in (authenticated) can access it.
    # Guests will get a 401/403 error.
    permission_classes = [IsAuthenticated]

    # 2. DYNAMIC FILTERING:
    def get_queryset(self):
        """
        This method overrides the default 'queryset'.
        It allows us to filter the data *based on the request*.
        """
        # Get the default queryset (the one with prefetch)
        qs = super().get_queryset()

        # Filter it down to *only* show orders where the 'user'
        # matches the currently logged-in user ('self.request.user').
        return qs.filter(user=self.request.user)


#create only handl post http , list handle get , list-create handle both


class ProductListCreateAPIView(generics.ListCreateAPIView):
    """
    Handles GET & POST requests to '/products/'
    """
    # We can apply a permanent filter to the queryset.
    # This endpoint will *only* ever show products with stock > 0.
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # we have 3 ways to modify the permissoins in restframework (get_queryser + class , get_permission +class , get_serializer + class)
    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class ProductDetailAPIView(generics.RetrieveAPIView):
    """
    Handles GET requests to '/products/<product_id>'
    'RetrieveAPIView' is pre-built to get a *single* object.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # By default, DRF looks for a URL variable named 'pk'.
    # Our urls.py uses 'product_id', so this line tells the
    # view to look for 'product_id' in the URL instead.
    lookup_url_kwarg = 'product_id'


#create only handl post http , list handle get , list-create handle both


class ProductInfoAPIView(APIView):
    """
    Handles GET requests to '/product/info/'
    This view uses the base 'APIView', so we have to build the
    'get' method ourselves. This is for when "generic" views aren't
    flexible enough, like when you need to combine data.
    """

    def get(self, request):
        # 1. Get the data from the database
        products = Product.objects.all()

        # 2. Build the custom dictionary that our 'ProductInfoSerializer' expects.
        # We run a separate query, 'aggregate()', to get the max price.
        data_to_serialize = {
            'products': products,
            'count': len(products),
            'max_price':
            products.aggregate(max_price=Max('price'))['max_price']
        }

        # 3. Serialize the *dictionary*, not the queryset.
        serializer = ProductInfoSerializer(data_to_serialize)

        # 4. Return the serialized data in a Response.
        return Response(serializer.data)


# @api_view(['GET'])
# def product_info(request):
# products = Product.objects.all()
# serializer = ProductInfoSerializer({
#     'products':
#     products,
#     'count':
#     len(products),
#     'max_price':
#     products.aggregate(max_price=Max('price'))['max_price']
# })
# return Response(serializer.data)

# #views.py file
# @api_view(['GET'])
# def product_list(request):
#     products = Product.objects.all()
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     serializer = ProductSerializer(product)
#     return Response(serializer.data)

# #views.py file
# @api_view(['GET'])
# def order_list(request):
#     orders = Order.objects.prefetch_related('items__product')
#     serializer = OrderSerializer(orders, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def user_list(request):
#     user = User.objects.all()
#     serializer = UserSerializer(user, many=True)
#     return Response(serializer.data)
