import datetime
from decimal import Decimal
from django.urls import reverse
from accounts.models import User
from django.utils import timezone
from django.core import paginator
from django.shortcuts import render
from django.contrib import messages
from products.models import Product
from referrals.models import Referral
from .models import Wallet, Transaction
from django.shortcuts import render, redirect
from datetime import datetime, timedelta, date
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import FundTransferForm, SubscriptionForm, ActivationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from KazubamarketApi.mixins import PaymentRequiredMixin, AdminRequiredMixin
from django.views.generic import DetailView, ListView, TemplateView, FormView, View

# from referrals.views import get_total_weekly_earn

# Create your views here.  
###############   REFER PAY VIEW    ###############
class PayReferralView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    template_name = 'payment/refer_pay.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(PayReferralView, self).get_context_data(*args, **kwargs)
        wallet = Wallet.objects.all().exclude(user = User.objects.get(admin = True))
        context["wallets"] = wallet
        return context
     
    def get_queryset(self):
        user = User.objects.all()
        return user
    
    def get_user(self):
        return self.request.user
    
def process_referral_bonus_payment(request, *args, **kwargs):
    wallet_list = request.POST.getlist('userwallet')
    reason = 'Payment of weekly refer bonus'
    admin_wallet = Wallet.objects.get(user = User.objects.get(admin = True))
    for i in wallet_list:
        wallet_balance = Wallet.objects.get(user = User.objects.get(username = i)).current_balance
        users_wallet = Wallet.objects.get(user = User.objects.get(username = i))
        users_wallet.transfer(wallet = admin_wallet, amount = wallet_balance, reason = reason, depositor = users_wallet, recipient = admin_wallet)
        users_wallet.weekly_earn_bonus = 0.00
        users_wallet.save()
    if request.method == 'POST':
        messages.add_message(request, messages.SUCCESS, "Amount Successfully Paid")
    wallet = Wallet.objects.all().exclude(user = User.objects.get(admin = True))
    context = {'wallets':wallet}
    return render(request, "payment/refer_pay.html", context)
    
###############   FUNDS TRANSFER VIEW    ###############
class TransferFundView(LoginRequiredMixin, FormView):
    form_class = FundTransferForm
    template_name = 'payment/transfer_form.html'
    
    def get_form_kwargs(self):
        kwargs = super(TransferFundView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_context_data(self, *args, **kwargs):
        context = super(TransferFundView, self).get_context_data(*args, **kwargs)
        context["vendor"] = self.get_user() 
        context["title"] = 'Wallet to Wallet Transfer'
        return context
    
    def form_valid(self, form):
        wallet = form.cleaned_data.get('wallets')
        amount = form.cleaned_data.get('amount')
        reason = form.cleaned_data.get('reason')
        user_wallet = Wallet.objects.get(user = self.request.user)
        try:
            user_wallet.transfer(wallet = wallet, amount = amount, reason = reason, depositor = user_wallet, recipient = wallet)
            messages.add_message(self.request, messages.SUCCESS, "Amount Successfully transfered")
        except:
            messages.add_message(self.request, messages.ERROR, "Insufficient Balance in wallets")
        return redirect('wallets:tranfer_fund')
    
    def get_user(self):
        return self.request.user
    
###############   REGISTRATION ACTIVATION VIEW    ###############
class RegistrationActivationView(LoginRequiredMixin, FormView):
    form_class = ActivationForm
    template_name = 'payment/wallet_sub_act_form.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(RegistrationActivationView, self).get_context_data(*args, **kwargs)
        context["vendor"] = self.get_user() 
        admin = User.objects.get(admin = True)
        admin_user_wallet = Wallet.objects.get(user = admin)
        context["title"] = 'Wallet Registration Activation'
        context['admin_user_wallet'] = admin_user_wallet
        return context
    
    def form_valid(self, form):
        user = self.get_user()
        wallet = form.cleaned_data.get('wallets')
        amount = form.cleaned_data.get('amount')
        reason = form.cleaned_data.get('reason')
        user_wallet = Wallet.objects.get(user = user)
        try:
            user_wallet.transfer(wallet = wallet, amount = amount, reason = reason, depositor = user_wallet, recipient = wallet)
            user.is_subscribe = True #Activate Subscription
            user.subscription_date = timezone.now().date()
            user_ref = Referral.objects.get(user = user)
            user_ref.has_paid_activation = True #Activate Subscription
            user_ref.package = amount #Registration Package
            user_ref.save()
            user.save()
            messages.add_message(self.request, messages.SUCCESS, "Registration Activation Amount Successfully Paid")
        except:
            messages.add_message(self.request, messages.ERROR, "Insufficient Balance in wallets to Activate")
        return redirect('wallets:wallet_activation')
    
    def get_user(self):
        return self.request.user
    
###############   MONTHLY SUBSCRIPTION VIEW    ###############
class SubscriptionView(LoginRequiredMixin, FormView):
    form_class = SubscriptionForm
    template_name = 'payment/wallet_sub_form.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(SubscriptionView, self).get_context_data(*args, **kwargs)
        context["vendor"] = self.get_user() 
        admin = User.objects.get(admin = True)
        admin_user_wallet = Wallet.objects.get(user = admin)
        context["title"] = 'Wallet Monthly Subscription'
        context['admin_user_wallet'] = admin_user_wallet
        return context
    
    def form_valid(self, form):
        wallet = form.cleaned_data.get('wallets')
        amount = form.cleaned_data.get('amount')
        reason = form.cleaned_data.get('reason')
        user_wallet = Wallet.objects.get(user = self.request.user)
        user = self.get_user()
        if int(amount) < 2 or int(amount) > 2:
            messages.add_message(self.request, messages.ERROR, "Subscription Amount Must be $2")
            return redirect('wallets:wallet_subscribe')
        else:
            try:
                user_wallet.transfer(wallet = wallet, amount = amount, reason = reason, depositor = user_wallet, recipient = wallet)
                user.is_subscribe = True # Activate Subscription
                user.subscription_date = timezone.now().date()
                user.save()
                user_products = Product.objects.filter(user = user)
                if user_products is not None:
                    for user_product in user_products:
                        user_product.active = True
                        user_product.save()
                messages.add_message(self.request, messages.SUCCESS, "Subscription Amount Successfully Paid")
            except:
                messages.add_message(self.request, messages.ERROR, "Insufficient Balance in wallets to Subscribe")
            return redirect('wallets:wallet_subscribe')
    
    def get_user(self):
        return self.request.user
    
###############   FAST TRACT VIEW    ###############
class FastTractPayView(LoginRequiredMixin, FormView):
    form_class = SubscriptionForm
    template_name = 'payment/wallet_sub_form.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(FastTractPayView, self).get_context_data(*args, **kwargs)
        context["vendor"] = self.get_user() 
        admin = User.objects.get(admin = True)
        admin_user_wallet = Wallet.objects.get(user = admin)
        context["title"] = 'Wallet Fast Tract ADs'
        context['admin_user_wallet'] = admin_user_wallet
        return context
    
    def form_valid(self, form):
        wallet = form.cleaned_data.get('wallets')
        amount = form.cleaned_data.get('amount')
        reason = form.cleaned_data.get('reason')
        user_wallet = Wallet.objects.get(user = self.request.user)
        user = self.get_user()
        if int(amount) < 10 or int(amount) > 10:
            messages.add_message(self.request, messages.ERROR, "Fast Tract Amount Must be $10")
            return redirect('wallets:wallet_activation')
        else:
            try:
                user_wallet.transfer(wallet = wallet, amount = amount, reason = reason, depositor = user_wallet, recipient = wallet)
                user_product_list = Product.objects.filter(user = user)
                for i in user_product_list:
                    i.featured = True
                    i.date_to_featured = timezone.now().date()
                    i.save()
                messages.add_message(self.request, messages.SUCCESS, "Fast Tract Amount Successfully Paid")
            except:
                messages.add_message(self.request, messages.ERROR, "Insufficient Balance in wallets to Pay")
            return redirect('wallets:wallet_activation')
    
    def get_user(self):
        return self.request.user
    
###############   TRANSACTION HISTORY LIST VIEW    ###############
class TransactionHistoryView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'payment/transaction_history.html'
    paginate_by = 10
    
    def get_context_data(self, *args, **kwargs):
        context = super(TransactionHistoryView, self).get_context_data(*args, **kwargs)
        page = self.request.GET.get("page")
        user_wallet = Wallet.objects.get(user = self.get_user())
        wallet_id = user_wallet.get_wallet_id()
        balance = user_wallet.get_current_balance()
        last_transfer_amount = user_wallet.get_last_transfer_amount()
        last_running_balance = user_wallet.get_last_running_balance()    
        user_transactions = Transaction.objects.filter(wallet = user_wallet).order_by('-created_at')
        user_transactions_paginator = paginator.Paginator(user_transactions, self.paginate_by)
        try:
            user_transactions_page_obj = user_transactions_paginator.page(page)
        except (paginator.PageNotAnInteger, paginator.EmptyPage):
            user_transactions_page_obj = user_transactions_paginator.page(1)
            
        # Total Money Sent
        if user_transactions.count() > 1:
            tot_sent = 0
            total_sent = 0
            for i in user_transactions:
                if i.amount < 0:
                    tot_sent += i.amount
            total_sent = tot_sent
            if user_transactions.count() >= 1:
                total_sent_split = str(total_sent).split('-')[1]
            else:
                total_sent_split = total_sent
        else:
            total_sent_split = 0.00
            
        # Total Money Recieved
        if user_transactions.count() > 1:
            tot_recieved = 0
            total_recieved = 0
            for i in user_transactions:
                if i.amount > 0:
                    tot_recieved += i.amount
            total_recieved = tot_recieved + user_wallet.weekly_earn_bonus_so_far
        else:
            total_recieved = 0.00
        
        # total_weekly_refer_earn = get_total_weekly_earn(self.request)
        # balance = float(balance) + float(total_weekly_refer_earn)
            
        context["balance"] = balance
        context['wallet_id'] = wallet_id
        context['total_recieved'] = total_recieved
        context['total_sent_split'] = total_sent_split
        context['last_transaction'] = last_transfer_amount
        context['last_running_balance'] = last_running_balance
        context["user_transactions_page_obj"] = user_transactions_page_obj
        return context
    
    # def get_weekly_refer_earn(self):
    #     weekly_refer_earn = self.request.session['total_weekly_refer_earn']
    #     return weekly_refer_earn
    
    def get_object(self):
        transaction = Transaction.objects.all()
        return transaction
    
    def get_user(self):
        return self.request.user

    
###############   TRANSACTION HISTORY DETAIL VIEW   ###############
class TransactionHistorySlugView(LoginRequiredMixin, DetailView):
    template_name = "payment/transaction_history_view.html"

    def get_context_data(self, *args, **kwargs):
        context = super(TransactionHistorySlugView, self).get_context_data(*args, **kwargs)
        return context

    def get_object(self, *args, **kwargs):
        transaction_id = self.kwargs.get('transaction_id')
        user_wallet = Wallet.objects.get(user = self.request.user)
        try:
            instance = Transaction.objects.get(wallet = user_wallet, transaction_id = transaction_id)
        except Transaction.DoesNotExist:
            raise Http404("Not found")
        except Transaction.MultipleObjectsReturned:
            qs = Transaction.objects.filter(wallet = user_wallet, transaction_id = transaction_id)
            instance = qs.first()
        except:
            raise Http404("Anonymous User Not Allowed")
        return instance

# ###############   REGISTRATION ACTIVATION VIEW    ###############
# class RegistrationActivationView(LoginRequiredMixin, FormView):
#     form_class = ActivationForm
#     template_name = 'payment/wallet_sub_act_form.html'
    
#     def get_context_data(self, *args, **kwargs):
#         context = super(RegistrationActivationView, self).get_context_data(*args, **kwargs)
#         context["vendor"] = self.get_user() 
#         admin = User.objects.get(admin = True)
#         admin_user_wallet = Wallet.objects.get(user = admin)
#         context["title"] = 'Wallet Registration Activation'
#         context['admin_user_wallet'] = admin_user_wallet
#         return context
    
#     def form_valid(self, form):
#         user = self.get_user()
#         wallets = form.cleaned_data.get('wallets')
#         amount = form.cleaned_data.get('amount')
#         reason = form.cleaned_data.get('reason')
#         user_wallet = Wallet.objects.get(user = user)
        
#         if int(amount) < 50 or int(amount) > 50:
#             messages.add_message(self.request, messages.ERROR, "Registration Amount Must be $50")
#             return redirect('wallets:wallet_activation')
#         else:
#             try:
#                 user_wallet.transfer(wallets = wallets, amount = amount, reason = reason, depositor = user_wallet, recipient = wallets)
#                 user.is_subscribe = True # Activate Subscription
#                 user.subscription_date = timezone.now().date()
#                 user_ref = Referral.objects.get(user = user)
#                 user_ref.has_paid_activation = True #Activate Subscription
#                 user_ref.save()
#                 user.save()
#                 messages.add_message(self.request, messages.SUCCESS, "Registration Activation Amount Successfully Paid")
#             except:
#                 messages.add_message(self.request, messages.ERROR, "Insufficient Balance in wallets to Activate")
#             return redirect('wallets:wallet_activation')
    
#     def get_user(self):
#         return self.request.user
    
    
# # First generation
# first_gens = []
# for i in users:
#     first_gen = i.referral.get_children()
#     first_gens += first_gen
#     print('This is first generation list: ',[i ,first_gen.count()])
# first_generation = first_gens
# print('this is the first: ',first_generation)

# # First generation
# sec_gen = []
# for i in first_generation:
#     sec_gen = i.get_children()
#     print('This is second generation list: ',[i ,sec_gen.count()])
# second_generation = sec_gen

    
# context["wallets"] = wallets
# context['first_generation'] = first_generation
# context['users'] = users