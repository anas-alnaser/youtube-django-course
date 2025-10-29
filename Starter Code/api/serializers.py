from rest_framework import serializers
from .models import *

# --- SERIALIZERS ---

# (This UserSerializer is commented out, but it's how you *would* serialize a user)
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'is_staff')


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializes the Product model.
    'ModelSerializer' is a magic-time-saver. It will automatically
    generate fields for you based on your model.
    """

    class Meta:
        model = Product  # 1. Link to the Product model

        fields = ('description', 'name', 'price', 'stock'
                  )  # 2. List the fields you want to include in the JSON.

    def validate_price(self, value):
        """
        This is a custom validation method.
        DRF automatically finds and runs any method named 'validate_<field_name>'.
        'value' is the incoming price from the user.
        """
        if value <= 0:
            # This 'ValidationError' will be sent back to the user as a
            # clean 400 Bad Request error.
            raise serializers.ValidationError("Price must be grater than 0")
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializes the OrderItem model.
    This serializer is special because it "flattens" data.
    """

    # These are NOT fields on the OrderItem model.
    # We use 'source=' to "reach through" the 'product' foreign key
    # and grab data from the related Product object.
    # This makes the API response much cleaner for the frontend.
    product_name = serializers.CharField(source='product.name')
    product_price = serializers.DecimalField(source='product.price',
                                             max_digits=10,
                                             decimal_places=2)

    class Meta:
        model = OrderItem
        # Note we can include 'item_subtotal' here!
        # The serializer is smart enough to find the '@property'
        # on the model and include it as a read-only field.
        fields = ('product_name', 'product_price', 'quantity', 'item_subtotal')


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializes the Order model. This is a "nested" serializer.
    """

    # --- NESTING ---
    # This is the most powerful part. It tells DRF:
    # "When you serialize an Order, find all the related items
    # (using the 'related_name="items"' from the model) and serialize
    # *each one* using the 'OrderItemSerializer'."
    # 'many=True' means we expect a list of items.
    # 'read_only=True' means this is for output only (we can't create orders this way).
    items = OrderItemSerializer(many=True, read_only=True)

    # --- CUSTOM FIELD ---
    # This adds a new field 'total_price' to the JSON that doesn't
    # exist on the model. 'SerializerMethodField' tells DRF:
    # "To get the value for this, go find a method named 'get_total_price'."
    total_price = serializers.SerializerMethodField()

    # (This is the commented-out UserSerializer from before)
    # user_info = UserSerializer(source='user', many=False, read_only=True)

    def get_total_price(self, obj):
        """
        This is the custom method that calculates the 'total_price'.
        'obj' is the Order object being serialized.
        
        1. 'obj.items.all()' - This works because of 'related_name="items"'.
        2. We use 'sum()' to add up all the 'item_subtotal' properties
           from all the OrderItems in this order.
        """
        order_items = obj.items.all()
        return sum(item.item_subtotal
                   for item in order_items)  # Fixed variable name

    class Meta:
        model = Order
        # We include 'user' (just the ID), 'items' (the nested list),
        # and 'total_price' (the calculated field) in our final JSON.
        fields = ('order_id', 'created_at', 'user', 'status', 'items',
                  'total_price')


class ProductInfoSerializer(serializers.Serializer):
    """
    This is a "manual" serializer, not a ModelSerializer.
    It doesn't map to any single model. It's used for custom,
    aggregated data. We are just defining the *shape* of the output.
    """
    # We expect a list of products, serialized with our ProductSerializer.
    products = ProductSerializer(many=True)
    # We expect a simple integer field.
    count = serializers.IntegerField()
    # We expect a simple float field.
    max_price = serializers.FloatField()
