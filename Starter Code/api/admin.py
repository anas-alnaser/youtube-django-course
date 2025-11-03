from django.contrib import admin
from api.models import Order, OrderItem, User, Product


# Register your models here.
class OrderItemInLine(admin.TabularInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInLine]


# No need to do the line & admin class for the default model just the one
# wiht complex query like the order and order item classes

admin.site.register(Order, OrderAdmin)
admin.site.register(Product)
admin.site.register(User)
# admin.site.register()
