from . import serializers
from products.models import Product
from categorys.models import Category
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status, mixins, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics, permissions, status, views
from KazubamarketApi.permissions import UserIsOwnerOrReadOnly, IsSubscribedUser
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView
from .serializers import ProductSerializer, ProductListSerializer, ProductDetailUpdateSerializer, ProductUserListSerializer

########## User Detail Delete API View ########## 
class ProductDeleteAPIView(DestroyAPIView):
    """
    Endpoint for Product Delete.
    Only a subscribed user has access.
    """
    allowed_methods = ('DELETE', 'OPTIONS', 'HEAD')
    serializer_class = ProductDetailUpdateSerializer
    permission_classes = (IsAuthenticated, IsSubscribedUser, UserIsOwnerOrReadOnly)
    
    def get_object(self):
        pk = self.kwargs["pk"]
        obj = get_object_or_404(Product, pk=pk)
        return obj
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

########## Product Detail Update API View ########## 
class ProductDetailUpdateAPIView(RetrieveUpdateAPIView):
    """
    Endpoint for Product Detail Update.
    Only a subscribed user has access.
    """
    allowed_methods = ('PUT', 'OPTIONS', 'HEAD')
    serializer_class = ProductDetailUpdateSerializer
    permission_classes = (IsAuthenticated, IsSubscribedUser, UserIsOwnerOrReadOnly,)
    
    def get_object(self):
        pk = self.kwargs["pk"]
        obj = get_object_or_404(Product, pk=pk)
        return obj
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

########## Product Detail API View ##########
class ProductDetailAPIView(RetrieveAPIView):
    """
    Endpoint for Product Detail.
    """
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]
    allowed_methods = ('GET', 'OPTIONS', 'HEAD')

    def get_queryset(self, *args, **kwargs):
        product_id = self.kwargs.get("pk")
        try:  
            qs = Product.objects.filter(pk = product_id)
            product_obj = qs
        except Product.DoesNotExist:
            return Response({"response":"Product does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        return product_obj

########## Product List API View ##########    
class ProductListAPIView(ListAPIView):
    """
    Endpoint for All Product List.
    """
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]
    allowed_methods = ('GET', 'OPTIONS', 'HEAD')

########## Product User Detail API View ##########
class ProductUserDetailAPIView(RetrieveAPIView):
    """
    Endpoint for User Product Detail.
    Only a subscribed user has access.
    """
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = (IsAuthenticated, IsSubscribedUser, UserIsOwnerOrReadOnly,)
    allowed_methods = ('GET', 'OPTIONS', 'HEAD')

    def get_queryset(self, *args, **kwargs):
        product_id = self.kwargs.get("pk")
        user = self.request.user
        try:  
            qs = Product.objects.filter(pk = product_id, user = self.request.user)
            product_obj = qs
        except Product.DoesNotExist:
            return Response({"response":"Product does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        return product_obj

########## Product User List API View ##########    
class ProductUserListAPIView(ListAPIView):
    """
    Endpoint for User Product List.
    Only a subscribed user has access.
    """
    allowed_methods = ('GET', 'OPTIONS', 'HEAD')
    serializer_class = ProductUserListSerializer
    permission_classes = [IsAuthenticated, IsSubscribedUser, UserIsOwnerOrReadOnly,]
    
    def get_queryset(self):
        user = self.request.user
        qs = Product.objects.filter(user=user)
        return qs

########## Product Registration API View ##########
class ProductCreateAPIView(CreateAPIView):
    """
    Endpoint for Product Create.
    Only a subscribed user has access.
    """
    serializer_class = ProductSerializer
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')
    permission_classes = [IsAuthenticated, IsSubscribedUser]
    parser_classes = (MultiPartParser, FormParser,)

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        return super(ProductCreateAPIView, self).perform_create(serializer)