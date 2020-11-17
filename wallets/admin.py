from django.contrib import admin
from .models import Wallet, Transaction

# Register your models here.
class WalletAdmin(admin.ModelAdmin):
    list_display = ['user', 'wallet_id', 'current_balance', 'weekly_earn_bonus']
    readonly_fields = ['wallet_id']
    list_filter = ['created_at']
admin.site.register(Wallet, WalletAdmin)

class TransactionAdmin(admin.ModelAdmin):
    list_display = ['wallet_id', 'amount', 'transaction_id', 'running_balance', 'current_balance', 'transaction_date', 'reason', 'depositor', 'recipient']
    list_filter = ['created_at']
    
    def transaction_date(self, obj):
        return obj.created_at
    
    def wallet_id(self, obj):
        return obj.wallet.user
admin.site.register(Transaction, TransactionAdmin)