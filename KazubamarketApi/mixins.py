from django.urls import reverse
from accounts.models import User
from referrals.models import Referral
from django.shortcuts import redirect
from django.utils.http import is_safe_url
from rest_framework.response import Response

###############   REQUEST ATTACH FORM   ###############
class RequestFormAttachMixin(object):
    def get_form_kwargs(self):
        kwargs = super(RequestFormAttachMixin, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

###############   NEXT URL   ###############
class NextUrlMixin(object):
    default_next = "/"
    def get_next_url(self):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        if is_safe_url(redirect_path, request.get_host()):
            return redirect_path
        return self.default_next
    
###############   SUBSCRIPTION REQUIRED   ###############
class PaymentRequiredMixin(object):
    redirect_unpaid_user = True
    def dispatch(self, request, *args, **kwargs):
        subscription_condition = User.objects.get(username = self.request.user).is_subscribe
        if self.redirect_unpaid_user and subscription_condition is False:
            return redirect(self.get_unpaid_user_redirect_url())
        return super().dispatch(request, *args, **kwargs)
    
    def get_unpaid_user_redirect_url(self):
        return reverse("accounts:vendor-home")
    
###############   ACTIVATION REQUIRED   ###############
class ActivationRequiredMixin(object):
    redirect_unactivated_user = True
    def dispatch(self, request, *args, **kwargs):
        activation_condition = Referral.objects.get(user = self.request.user).has_paid_activation
        if self.redirect_unactivated_user and activation_condition is False:
            return redirect(self.get_unactivated_user_redirect_url())
        return super().dispatch(request, *args, **kwargs)
    
    def get_unactivated_user_redirect_url(self):
        return reverse("accounts:vendor-home")

###############   ADMIN REQUIRED   ###############
class AdminRequiredMixin(object):
    redirect_user_except_Admin = True
    def dispatch(self, request, *args, **kwargs):
        admin_user = User.objects.get(username = self.request.user).admin
        if self.redirect_user_except_Admin and admin_user is False:
            return Response({"User Roles": ["Admin required"]}, status=status.HTTP_400_BAD_REQUEST)
        return super().dispatch(request, *args, **kwargs)
    
    def get_user_redirect_url(self):
        return reverse("accounts:vendor-home")