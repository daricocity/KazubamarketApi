import uuid
from decimal import Decimal
from django.db import models
from django.urls import reverse
from accounts.models import User
from django.db.models.signals import post_save, pre_save
from KazubamarketApi.utils import unique_transaction_id_generator
from wallets.errors import InsufficientBalance, TransactionDoesNotExist

# Create your models here.
###############  WALLET QUERYSET  ###############
class WalletQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active = True)
 
###############  WALLET MANAGER  ###############   
class WalletManager(models.Manager):
    def get_queryset(self):
        return WalletQuerySet(self.model, using = self._db)

    def all(self):
        return self.get_queryset().active()
    
###############   WALLET    ###############
class Wallet(models.Model):
    user = models.ForeignKey(User, null = True, blank = True, on_delete = models.CASCADE)
    wallet_id = models.UUIDField(default = uuid.uuid4, editable = False, unique = True)
    current_balance = models.DecimalField(decimal_places = 2, max_digits = 20, default = 00.00)
    weekly_earn_bonus = models.DecimalField(decimal_places = 2, max_digits = 20, default = 00.00)
    weekly_retained_earn_bonus = models.DecimalField(decimal_places = 2, max_digits = 20, default = 00.00)
    weekly_earn_bonus_so_far = models.DecimalField(decimal_places = 2, max_digits = 20, default = 00.00)
    created_at = models.DateTimeField(auto_now_add = True)
    active = models.BooleanField(default = True)
    
    objects = WalletManager()
    
    def __str__(self):
        return str(self.user)
    
    def deposit(self, amount, reason, depositor):
        amount = Decimal(amount)
        self.transaction_set.create(amount = amount, running_balance = self.current_balance + amount, current_balance = self.current_balance, reason = reason, depositor = depositor)
        self.current_balance += amount
        self.save()
        
    def withdraw(self, amount, reason, recipient):
        amount = Decimal(amount)
        if amount > (self.current_balance):
            raise InsufficientBalance('This wallets has insufficient balance.')
        self.transaction_set.create(amount =- amount, running_balance = self.current_balance - amount, current_balance = self.current_balance, reason = reason, recipient = recipient)
        self.current_balance -= amount
        self.save()
        
    def transfer(self, wallet, amount, reason, depositor, recipient):
        self.withdraw(amount, reason, recipient)
        wallet.deposit(amount, reason, depositor)
        
    def get_current_balance(self):
        return self.current_balance
    
    def get_wallet_id(self):
        return self.wallet_id
    
    def get_last_transfer_amount(self):
        transaction = Transaction.objects.filter(wallet = self.pk).exists()
        if transaction:
            trans = Transaction.objects.filter(wallet = self.pk).last().amount
            return trans
        return 0.00
    
    def get_running_balance(self):
        transaction = Transaction.objects.filter(wallet = self.pk).exists()
        if transaction:
            trans = Transaction.objects.get(wallet = self.pk).running_balance
            return trans
        return 0.00
    
    # The value of the wallets at the time of this transaction. Useful for displaying transaction history.
    def get_last_running_balance(self):
        try:
            transaction = self.get_running_balance() + self.get_last_transfer_amount()
        except Transaction.MultipleObjectsReturned:
            qs = Transaction.objects.filter(wallet = self.pk)
            transaction =  qs.last().running_balance + self.get_last_transfer_amount()
        except Transaction.DoesNotExist:
            raise TransactionDoesNotExist('No Transaction Yet.')
        return transaction
    
###############  TRANSACTION QUERYSET  ###############
class TransactionQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active = True)

    # Get Individual Objects in Database
    def get_id(self, id):
        qs = self.get_queryset().filter(id = id)
        if qs.count() == 1:
            return qs.first()
        return None
 
###############  TRANSACTION MANAGER  ###############   
class TransactionManager(models.Manager):
    def get_queryset(self):
        return TransactionQuerySet(self.model, using = self._db)

    def all(self):
        return self.get_queryset().active()
    
###############   TRANSACTION    ###############
class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, null = True, blank = True, on_delete = models.SET_NULL)
    transaction_id = models.CharField(max_length = 20, blank = True)
    amount = models.DecimalField(max_digits = 14, decimal_places = 2)
    current_balance = models.DecimalField(decimal_places = 2, max_digits = 20, default = 00.00)
    running_balance = models.DecimalField(max_digits = 14, decimal_places = 2)
    depositor = models.CharField(max_length = 50, blank = True, null = True)
    recipient = models.CharField(max_length = 50, blank = True, null = True)
    reason = models.TextField(blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    active = models.BooleanField(default = True)
    
    objects = TransactionManager()
    
    def get_transaction_detail_url(self):
        return reverse("wallets:wallet_transaction_detail", kwargs={"transaction_id": self.transaction_id})
    
    def __str__(self):
        return str(self.wallet)
    
def transaction_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.transaction_id:
        instance.transaction_id = unique_transaction_id_generator(instance)
pre_save.connect(transaction_pre_save_receiver, sender = Transaction)