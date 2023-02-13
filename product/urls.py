from django.urls import path, include
from rest_framework.routers import DefaultRouter
from product.views import ProductViewSet

app_name = 'product'

router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls))
]
