from django.urls import path
from . import views

urlpatterns = [
    path('product/', views.product_list),
    path('product/<int:pk>', views.product_detail),
    path('order/', views.order_list),
    # path('user/', views.user_list)
    path('product/info/', views.product_info),
]
