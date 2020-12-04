from django.urls import path
from wallets.api.views import WalletListAPIView, FundTransferAPIView, ActivationAPIView, SubscriptionAPIView, TransactionAPIView, AllTransactionAPIView, TransactionDetailAPIView, WalletUserAPIView

app_name = 'wallet'

urlpatterns = [
    path('wallet/', WalletUserAPIView.as_view(), name = 'wallet'),
    path('activate/', ActivationAPIView.as_view(), name = 'activate'),
    path('transfer/', FundTransferAPIView.as_view(), name = 'transfer'),
    path('subscribe/', SubscriptionAPIView.as_view(), name = 'subscribe'),
    path('all_wallet/', WalletListAPIView.as_view(), name = 'wallet-all'),
    path('transactions/', TransactionAPIView.as_view(), name = 'transactions'),
    path('all_transactions/', AllTransactionAPIView.as_view(), name = 'all-transactions'),
    path('transaction/<pk>/', TransactionDetailAPIView.as_view(), name = 'transaction-detail'),
]