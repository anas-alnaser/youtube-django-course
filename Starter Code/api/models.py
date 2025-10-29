from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid  # Used for creating unique order IDs


class User(AbstractUser):
    """
    A custom user model.
    
    By inheriting from 'AbstractUser', this model automatically gets all
    the fields for a standard Django user (username, password, email, etc.).
    
    Using 'pass' here is a common practice. It means "use the default
    AbstractUser fields for now, but I've set it up so I *can*
    add more fields (like a phone number) in the future."
    """
    pass


class Product(models.Model):
    """
    Represents a single product that can be sold.
    """
    # A simple text field for the product's name.
    name = models.CharField(max_length=200)

    # A large text block for the description.
    description = models.TextField()

    # 'DecimalField' is crucial for money to avoid floating-point rounding errors.
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # 'PositiveIntegerField' ensures the stock can't be negative.
    stock = models.PositiveIntegerField()

    # An optional field for a product image.
    # 'upload_to=' specifies the sub-directory in your 'media' folder.
    image = models.ImageField(upload_to='product/', blank=True, null=True)

    @property
    def in_stock(self):
        """
        A "calculated property" that is not stored in the database.
        It's calculated on-the-fly when you access it.
        This lets you simply check 'product.in_stock' (True/False).
        """
        return self.stock > 0

    def __str__(self):
        """
        A "magic method" that provides a human-readable name for the object.
        This is what you'll see in the Django admin panel.
        """
        return self.name


class Order(models.Model):
    """
    Represents a single order placed by a user, which can contain
    multiple OrderItems.
    """

    class StatusChoices(models.TextChoices):
        """
        An "enum" class to define standardized choices for the order status.
        This prevents typos and keeps data consistent.
        """
        PENDING = 'Pending'
        CONFIRMED = 'Confirmed'
        CANCELLED = 'Cancelled'

    # 'UUIDField' is a great primary key for orders. It's a long, random
    # ID, so users can't guess other order IDs (e.g., /orders/1, /orders/2).
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    # 'ForeignKey' creates a "many-to-one" link.
    # One User can have MANY Orders.
    # 'on_delete=models.CASCADE' means "if the user is deleted, delete all their orders."
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # 'auto_now_add=True' automatically sets this to the current time
    # *only* when the order is first created.
    created_at = models.DateTimeField(auto_now_add=True)

    # This field uses the 'StatusChoices' class for its options.
    status = models.CharField(max_length=10,
                              choices=StatusChoices.choices,
                              default=StatusChoices.PENDING)

    # This 'ManyToManyField' links Orders and Products.
    # BUT, we need to store *how many* of each product (the quantity).
    # The 'through="OrderItem"' tells Django: "Don't make a simple link table.
    # Use the 'OrderItem' model as the intermediary to store the extra data."
    product = models.ManyToManyField(Product,
                                     through="OrderItem",
                                     related_name='orders')

    def __str__(self):
        return f"Order {self.order_id} by {self.user.username}"


class OrderItem(models.Model):
    """
    This is the "through" model (or "join table").
    It connects a specific Order to a specific Product and stores
    the 'quantity' for that pairing.
    """

    # Links this item back to its parent Order.
    # We add 'related_name="items"' here. This is *very important*.
    # It allows us to go from an Order object and get all its items
    # by simply writing: 'my_order.items.all()'.
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              related_name='items')

    # Links this item to the specific Product.
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    # Stores how many of this product are in this order.
    quantity = models.PositiveIntegerField()

    @property
    def item_subtotal(self):
        """
        Another calculated property. This is the business logic
        for calculating the subtotal of this specific line item.
        """
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} * {self.product.name} in order {self.order.order_id}"
