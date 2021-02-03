from django.urls import path
from orders.api.views import OrderUserListAPIView, OrderCreateAPIView, OrderUserDetailAPIView

app_name = 'order'

urlpatterns = [
    path('list/', OrderUserListAPIView.as_view(), name = 'order-list'),
    path('create/', OrderCreateAPIView.as_view(), name = 'order-create'),
    path('detail/', OrderUserDetailAPIView.as_view(), name = 'order-detail'),
]