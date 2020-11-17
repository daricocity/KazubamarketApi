from django.conf.urls import url
from .views import TransferFundView, SubscriptionView, TransactionHistoryView, TransactionHistorySlugView, RegistrationActivationView, FastTractPayView, PayReferralView, process_referral_bonus_payment

app_name = 'wallets'

urlpatterns = [
    url(r'^pay/$', process_referral_bonus_payment, name = 'p_r_b_p'),
    url(r'^pay/$', PayReferralView.as_view(), name = 'pay_referral'),
    url(r'^transfer/$', TransferFundView.as_view(), name = 'tranfer_fund'),
    url(r'^subscribe/$', SubscriptionView.as_view(), name = 'wallet_subscribe'),
    url(r'^fast_tract/$', FastTractPayView.as_view(), name = 'wallet_fast_tract'),
    url(r'^transactions/$', TransactionHistoryView.as_view(), name = 'wallet_transaction'),
    url(r'^activation/$', RegistrationActivationView.as_view(), name = 'wallet_activation'),
    url(r'^transactions/(?P<transaction_id>[\w-]+)/$', TransactionHistorySlugView.as_view(), name = 'wallet_transaction_detail'),
]