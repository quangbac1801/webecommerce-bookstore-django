from django.shortcuts import render
from .serializers import CategorySerializer, ProductSerializer, UserSerializer, OrderSerializer
from myapp.models import *
from rest_framework.decorators import action
from rest_framework import viewsets, permissions, generics
from rest_framework.parsers import MultiPartParser

# Create your views here.
##########API############
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(active=True)
    serializer_class = CategorySerializer

    # def get_permissions(self):
    #     if self.action == "list":
    #         return [permissions.AllowAny()]
    #     return [permissions.IsAuthenticated()]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

    # def get_permissions(self):
    #     if self.action =="list":
    #         return [permissions.AllowAny()]
    #     return [permissions.IsAuthenticated()]


class UserViewSet(viewsets.ViewSet, 
                  generics.ListAPIView, 
                  generics.CreateAPIView, 
                  generics.RetrieveAPIView):
    queryset=User.objects.filter(is_active=True)
    serializer_class= UserSerializer
    parser_class=[MultiPartParser ]

    # def permissions(self):
    #     if self.action == 'retrieve':
    #         return [permissions.IsAuthenticated()]
    #     return [permissions.AllowAny()]
    
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    # def get_permissions(self):
    #     if self.action == "list":
    #         return [permissions.AllowAny()]
    #     return [permissions.IsAuthenticated()]