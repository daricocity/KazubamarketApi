from django.urls import path
from categorys.api.views import CategoryCreateAPIView, CategoryUserListAPIView, CategoryUserDetailAPIView, CategoryDetailUpdateAPIView, CategoryListAPIView

app_name = 'category'

urlpatterns = [
    path('all/', CategoryListAPIView.as_view(), name = 'cat-all'),
    path('list/', CategoryUserListAPIView.as_view(), name = 'cat-list'),
    path('create/', CategoryCreateAPIView.as_view(), name = 'cat-create'),
    path('<pk>/', CategoryUserDetailAPIView.as_view(), name = 'cat-detail'),
    path('<pk>/edit/', CategoryDetailUpdateAPIView.as_view(), name = 'cat-update'),
]