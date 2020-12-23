from accounts.models import User
from django.utils import timezone
from products.models import Product
from referrals.models import Referral
from rest_framework import serializers
from wallets.models import Wallet, Transaction

########## TRANSACTION SERIALIZER ##########
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'wallet', 'transaction_id', 'amount', 'current_balance', 'running_balance', 'depositor', 'recipient', 'reason', 'created_at']

########## WALLET SERIALIZER ##########
class WalletSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Wallet
        fields = ['id', 'user', 'username', 'current_balance', 'weekly_earn_bonus', 'weekly_earn_bonus_so_far']

    def get_username(self, obj):
        return obj.user.username

########## MONTHLY SUBSCRIPTON SERIALIZER ##########
class SubcriptionSerializer(serializers.ModelSerializer):
    amount = serializers.CharField()
    reason = serializers.CharField()

    class Meta:
        model = Transaction
        fields = ['amount', 'reason']

    def save(self):
        user = self.get_object()
        amount = self.validated_data["amount"]
        reason = self.validated_data['reason']
        user_wallet = Wallet.objects.get(user = user)
        wallet = Wallet.objects.get(user = User.objects.get(admin = True))
        if int(amount) < 2 or int(amount) > 2:
            raise serializers.ValidationError({'amount': 'Subscription Amount Must be $2'})
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
            except:
                raise serializers.ValidationError({'amount': 'Insufficient Balance in wallet'})

    def get_object(self):
        user = self.context['request'].user
        return user

########## REGISTRATION ACTIVATION SERIALIZER ##########
REG_PACKAGE = (
    ('$20 Package', '20'),
    ('$50 Package', '50'),
    ('$100 Package', '100'),
)

class ActivationSerializer(serializers.ModelSerializer):
    package = serializers.ChoiceField(choices=REG_PACKAGE)
    reason = serializers.CharField()

    class Meta:
        model = Transaction
        fields = ['package', 'reason']

    def save(self):
        user = self.get_object()
        package = self.validated_data["package"]
        reason = self.validated_data['reason']
        user_wallet = Wallet.objects.get(user = user)
        wallet = Wallet.objects.get(user = User.objects.get(admin = True))
        if package == '$20 Package':
            amount = 20
        elif package == '$50 Package':
            amount = 50
        elif package == '$100 Package':
            amount = 100
        try:
            user_wallet.transfer(wallet = wallet, amount = amount, reason = reason, depositor = user_wallet, recipient = wallet)
            user.is_subscribe = True #Activate Subscription
            user.subscription_date = timezone.now().date()
            user_ref = Referral.objects.get(user = user)
            user_ref.has_paid_activation = True #Activate Subscription
            user_ref.package = amount #Registration Package
            user_ref.save()
            user.save()
        except:
            raise serializers.ValidationError({'amount': 'Insufficient Balance in wallet'})

    def get_object(self):
        user = self.context['request'].user
        return user

    # def get_object(self):
    #     user =  None
    #     request = self.context.get('request')
    #     if request and hasattr(request, 'user'):
    #         user = request.user
    #     return user

########## FUND TRANSFER SERIALIZER ##########
class WalletFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        request = self.context.get('request', None)
        queryset = super(WalletFilteredPrimaryKeyRelatedField, self).get_queryset()
        if not request or not queryset:
            return None
        return queryset

class TransferSerializer(serializers.ModelSerializer):
    wallet = WalletFilteredPrimaryKeyRelatedField(queryset = Wallet.objects.all(), many = False)
    amount = serializers.CharField()
    reason = serializers.CharField()

    class Meta:
        model = Transaction
        fields = ['wallet', 'amount', 'reason']

    def save(self):
        user = self.get_object()
        wallet = self.validated_data["wallet"]
        amount = self.validated_data["amount"]
        reason = self.validated_data['reason']
        user_wallet = Wallet.objects.get(user = user)
        try:
            user_wallet.transfer(wallet = wallet, amount = amount, reason = reason, depositor = user_wallet, recipient = wallet)
        except:
            raise serializers.ValidationError({'amount': 'Insufficient Balance in wallets'})

    def get_object(self):
        user = self.context['request'].user
        return user