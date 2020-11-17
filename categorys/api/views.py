from categorys.models import Category
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, mixins, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from KazubamarketApi.permissions import UserIsOwnerOrReadOnly, IsSubscribedUser
from .serializers import CategorySerializer, CategoryUserListSerializer, CategoryDetailUpdateSerializer, CategoryListSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView

########## User List API View ##########    
class CategoryListAPIView(ListAPIView):
    """
    Endpoint for All Category List.
    """
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    permission_classes = [permissions.AllowAny]
    allowed_methods = ('GET', 'OPTIONS', 'HEAD')

########## Category Detail Update API View ########## 
class CategoryDetailUpdateAPIView(RetrieveUpdateAPIView):
    """
    Endpoint for Category Detail Update.
    Only a suscribed user has access.
    """
    allowed_methods = ('PUT', 'OPTIONS', 'HEAD')
    serializer_class = CategoryDetailUpdateSerializer
    permission_classes = (IsAuthenticated, IsSubscribedUser, UserIsOwnerOrReadOnly,)
    
    def get_object(self):
        pk = self.kwargs["pk"]
        obj = get_object_or_404(Category, pk=pk)
        return obj
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

########## User Detail API View ##########
class CategoryUserDetailAPIView(RetrieveAPIView):
    """
    Endpoint for Category User Detail.
    Only a suscribed user has access.
    """
    queryset = Category.objects.all()
    serializer_class = CategoryUserListSerializer
    permission_classes = (IsAuthenticated, IsSubscribedUser, UserIsOwnerOrReadOnly,)
    allowed_methods = ('GET', 'OPTIONS', 'HEAD')

    def get_queryset(self, *args, **kwargs):
        category_id = self.kwargs.get("pk")
        user = self.request.user
        try:  
            qs = Category.objects.filter(pk = category_id, user = self.request.user)
            category_obj = qs
        except Category.DoesNotExist:
            return Response({"response":"Category does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        return category_obj

########## Category List API View ##########    
class CategoryUserListAPIView(ListAPIView):
    """
    Endpoint for Category User's List.
    Only a suscribed user has access.
    """
    allowed_methods = ('GET', 'OPTIONS', 'HEAD')
    serializer_class = CategoryUserListSerializer
    permission_classes = [IsAuthenticated, IsSubscribedUser, UserIsOwnerOrReadOnly,]
    
    def get_queryset(self):
        user = self.request.user
        qs = Category.objects.filter(user = user)
        return qs

########## Category Create API View ##########
class CategoryCreateAPIView(CreateAPIView): # create-only endpoint
    """
    Endpoint for Category Create.
    Only a suscribed user has access.
    """
    serializer_class = CategorySerializer
    # queryset = Category.objects.all()
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')
    permission_classes = [IsAuthenticated, IsSubscribedUser]
    
    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        return super(CategoryCreateAPIView, self).perform_create(serializer)