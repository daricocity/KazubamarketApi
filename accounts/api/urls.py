from django.urls import path, include
from accounts.api.jwt.views import TokenObtainPairView
from accounts.api.views import UserRegistrationAPIView, UserListAPIView, UserDetailAPIView, UserDetailUpdateAPIView, ChangePasswordView

app_name = 'accounts'

urlpatterns = [
    path('users/', UserListAPIView.as_view(), name = 'users-list'),
    path('login/', TokenObtainPairView.as_view(), name = 'user-login'),
    path('user/<pk>/', UserDetailAPIView.as_view(), name = 'user-detail'),
    path('signup/', UserRegistrationAPIView.as_view(), name = 'user-signup'),
    path('user/<pk>/edit/', UserDetailUpdateAPIView.as_view(), name='update-detail'),
    path('user/<username>/change_password/', ChangePasswordView.as_view(), name = 'user-change-password'),
]

# from knox.views import LogoutView