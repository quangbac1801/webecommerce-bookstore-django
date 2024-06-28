from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet,UserViewSet, OrderViewSet


router = DefaultRouter()
router.register('category', CategoryViewSet)
router.register("products", ProductViewSet)
router.register("user", UserViewSet)
router.register("order", OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]