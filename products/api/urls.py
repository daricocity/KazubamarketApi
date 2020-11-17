from django.urls import path
from products.api.views import ProductCreateAPIView, ProductListAPIView, ProductUserListAPIView, ProductUserDetailAPIView, ProductDetailAPIView, ProductDetailUpdateAPIView, ProductDeleteAPIView

app_name = 'product'

urlpatterns = [
    path('all/', ProductListAPIView.as_view(), name = 'pro-all'),
    path('list/', ProductUserListAPIView.as_view(), name = 'pro-list'),
    path('create/', ProductCreateAPIView.as_view(), name = 'pro_create'),
    path('<pk>/delete/', ProductDeleteAPIView.as_view(), name='pro-delete'),
    path('all/<pk>/', ProductDetailAPIView.as_view(), name = 'pro-detail'),
    path('<pk>/', ProductUserDetailAPIView.as_view(), name = 'pro-user-detail'),
    path('<pk>/edit/', ProductDetailUpdateAPIView.as_view(), name = 'pro-update'),
]
