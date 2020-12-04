from rest_framework.views import APIView
from rest_framework.response import Response
from wallets.models import Wallet, Transaction
from rest_framework.permissions import IsAuthenticated
from KazubamarketApi.permissions import UserIsOwnerOrReadOnly, IsAdminUser
from rest_framework import status, mixins, permissions, generics, views
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView, DestroyAPIView
from .serializers import WalletSerializer, TransferSerializer, ActivationSerializer, SubcriptionSerializer, TransactionSerializer

########## ALL TRANSACTION LIST API VIEW ##########    
class AllTransactionAPIView(ListAPIView):
    """
    Endpoint for All Transaction List View only by Admin.
    """
    allowed_methods = ('GET', 'OPTIONS', 'HEAD')
    serializer_class = TransactionSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        user = self.request.user
        qs = None
        if user.admin:
            qs = Transaction.objects.all().order_by('-created_at')
        return qs

########## USER TRANSACTION DETAIL API VIEW ##########
class TransactionDetailAPIView(RetrieveAPIView):
    """
    Endpoint for User's Transaction Detail.
    """
    serializer_class = TransactionSerializer
    allowed_methods = ('GET', 'OPTIONS', 'HEAD')
    permission_classes = [IsAuthenticated,]

    def get_queryset(self, *args, **kwargs):
        slug = self.kwargs.get("pk")
        trans_user = Wallet.objects.get(user = self.request.user)
        try:  
            qs = Transaction.objects.filter(pk = slug, wallet = trans_user)
            trans_obj = qs
        except Transaction.DoesNotExist:
            return Response({"response": "Transaction does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        return trans_obj

########## TRANSACTION LIST API VIEW ##########    
class TransactionAPIView(ListAPIView):
    """
    Endpoint for User's Transaction List.
    """
    allowed_methods = ('GET', 'OPTIONS', 'HEAD')
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated,]
    
    def get_queryset(self):
        user_wallet = Wallet.objects.get(user = self.get_user())
        qs = Transaction.objects.filter(wallet = user_wallet).order_by('-created_at')
        return qs

    def get_user(self):
        return self.request.user

########## MONTHLY SUBSCRIPTION API VIEW ##########
class SubscriptionAPIView(CreateAPIView):
    """
    Endpoint for Shop Monthly Subcription.
    """
    serializer_class = SubcriptionSerializer
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        return super(SubscriptionAPIView, self).perform_create(serializer)

########## ACTIVAION API VIEW ##########
class ActivationAPIView(CreateAPIView):
    """
    Endpoint for User's Registration Activation.
    """
    serializer_class = ActivationSerializer
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        return super(ActivationAPIView, self).perform_create(serializer)

########## TRANSFER API VIEW ##########
class FundTransferAPIView(CreateAPIView):
    """
    Endpoint for Fund Transfer.
    """
    serializer_class = TransferSerializer
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        return super(FundTransferAPIView, self).perform_create(serializer)

########## Product User List API View ##########    
class WalletUserAPIView(ListAPIView):
    """
    Endpoint for User Product List.
    Only a suscribed user has access.
    """
    allowed_methods = ('GET', 'OPTIONS', 'HEAD')
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated, UserIsOwnerOrReadOnly,]
    
    def get_queryset(self):
        user = self.request.user
        qs = Wallet.objects.filter(user=user)
        return qs

########## WALLET LIST API VIEW ##########    
class WalletListAPIView(ListAPIView):
    """
    Endpoint for User's Wallet List.
    """
    allowed_methods = ('GET', 'OPTIONS', 'HEAD')
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated,]
    
    def get_queryset(self):
        qs = Wallet.objects.all()
        return qs