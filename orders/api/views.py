from rest_framework import status
from orders.models import Order, Cart
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from KazubamarketApi.permissions import UserIsOwnerOrReadOnly
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from .serializers import OrderSerializer, OrderListSerializer, OrderDetailSerializer

########## Order Detail API View ##########
class OrderUserDetailAPIView(ListAPIView):
    """
    Endpoint for Order User's Detail.
    Only a Authenticated user has access.
    """
    allowed_methods = ('GET', 'OPTIONS', 'HEAD')
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated, UserIsOwnerOrReadOnly,]

    def get_queryset(self):
        user = self.request.user
        qs = Cart.objects.filter(user = user)
        return qs

########## Order List API View ##########
class OrderUserListAPIView(ListAPIView):
    """
    Endpoint for Order User's List.
    Only a Authenticated user has access.
    """
    allowed_methods = ('GET', 'OPTIONS', 'HEAD')
    serializer_class = OrderListSerializer
    permission_classes = [IsAuthenticated, UserIsOwnerOrReadOnly,]

    def get_queryset(self):
        user = self.request.user
        qs = Order.objects.filter(user = user)
        return qs

########## Order Create API View ##########
class OrderCreateAPIView(CreateAPIView):  # create-only endpoint
    """
    Endpoint for Category Create.
    Only an Authenticated user has access.
    """
    serializer_class = OrderSerializer
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')
    permission_classes = [IsAuthenticated,]

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        return super(OrderCreateAPIView, self).perform_create(serializer)