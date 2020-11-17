from django.urls import path
from referrals.api.views import ReferralAPIView

app_name = 'referral'

urlpatterns = [
    path('<pk>/', ReferralAPIView.as_view(), name = 'referral'),
]