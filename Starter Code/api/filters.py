import django_filters
from api.models import Product, Order
from rest_framework import filters


class InStockFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(stock__gt=0)


class ProductFilter(django_filters.FilterSet):
    created_at = django_filters.DateFilter(field_name='created_at__date')

    class Meta:
        model = Product
        fields = {
            'name': ['iexact', 'icontains'],
            'price': ['exact', 'lt', 'gt', 'range']
            #use it product?price_ls=num , price_gt =num
            #price_range=100_350
            #name__contains=substring
        }


class OrderFilter(django_filters.FilterSet):

    class Meta:
        model = Order
        fields = {'status': ['exact'], 'created_at': ['exact', 'lt', 'gt']}
