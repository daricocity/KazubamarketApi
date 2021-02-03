"""KazubamarketApi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title = 'Kazubamarket API',)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/docs/', schema_view),
    path('api/order/', include("orders.api.urls", namespace = 'order_api')),
    path('api/wallet/', include("wallets.api.urls", namespace = 'wallet_api')),
    path('api/account/', include("accounts.api.urls", namespace = 'account_api')),
    path('api/product/', include("products.api.urls", namespace = 'product_api')),
    path('api/category/', include("categorys.api.urls", namespace = 'category_api')),
    path('api/referral/', include("referrals.api.urls", namespace = 'referral_api')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
