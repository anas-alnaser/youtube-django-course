from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('product/', views.ProductListCreateAPIView.as_view()),
    path('product/<int:product_id>/', views.ProductDetailAPIView.as_view()),
    path('product/info/', views.ProductInfoAPIView.as_view()),
]

router = DefaultRouter()
router.register('orders', views.OrderViewSet)
urlpatterns += router.urls
