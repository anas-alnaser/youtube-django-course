from django.urls import path
from . import views

urlpatterns = [
    path('product/', views.ProductListCreateAPIView.as_view()),
    path('product/<int:product_id>', views.ProductDetailAPIView.as_view()),
    path('order/', views.OrderListAPIView.as_view()),
    path('product/info/', views.ProductInfoAPIView.as_view()),
    path('user-orders/',
         views.UserOrderListAPIView.as_view(),
         name='user-orders'),
]
