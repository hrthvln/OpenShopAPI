from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet

# Buat router dan daftarkan ViewSet kita
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    # Sertakan URL dari router
    path('', include(router.urls)),
    # Tambahkan nama untuk detail produk agar bisa digunakan di HATEOAS
    # Ini dibuat otomatis oleh router, tapi kita beri nama eksplisit untuk reverse()
    path('products/<uuid:pk>/', ProductViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='product-detail'),
]
