from accounts.models import User
from wallets.models import Wallet
from referrals.models import Link, Referral
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import serializers, exceptions
from django.utils.translation import ugettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken, SlidingToken, UntypedToken

########## User Change Password Serializer ##########
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

########## User Detail Update Serializer ##########
class UserDetailUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True, required=False, allow_blank=True, initial="current username")
    class Meta:
        model = User
        fields = [
            'username','email','full_name','phone_number','occupation','address','bank_account_name','bank_account_number','bank_name'
        ]
        
    def update(self, instance, validated_data):
        instance.email = validated_data.get('email',instance.email)
        instance.full_name = validated_data.get('full_name',instance.full_name)
        instance.phone_number = validated_data.get('phone_number',instance.phone_number)
        instance.occupation = validated_data.get('occupation',instance.occupation)
        instance.address = validated_data.get('address',instance.address)
        instance.bank_account_name = validated_data.get('bank_account_name',instance.bank_account_name)
        instance.bank_account_number = validated_data.get('bank_account_number',instance.bank_account_number)
        instance.bank_name = validated_data.get('bank_name',instance.bank_name)
        instance = super().update(instance, validated_data)
        return instance

########## User Detail Serializer ##########
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name', 'phone_number', 'occupation', 'address']

########## User List Serializer ##########
class UserListSerializer(serializers.ModelSerializer):
    has_paid_activation = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name', 'phone_number', 'occupation', 'bank_account_name','bank_account_number','bank_name', 'address', 'admin', 'is_subscribe', 'has_paid_activation']

    def get_has_paid_activation(self, obj):
        return obj.referral.has_paid_activation

########## User Registration Serializer ##########
class LinkSerializer(serializers.ModelSerializer):

    class meta:
        model = Link
        fields = ['user', 'referral_id', 'token']

class UserRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    referral_id = serializers.CharField(write_only=True)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'full_name', 'email', 'password', 'confirm_password', 'referral_id']
        
    def save(self):
        # Params
        username = self.validated_data["username"]
        full_name = self.validated_data['full_name']
        email = self.validated_data['email']
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']
        referral_id = self.validated_data['referral_id']
        user = User(username = username, full_name = full_name, email = email)
    
        # Validating
        username_qs = User.objects.filter(username = username).exists()
        link = Link.objects.filter(referral_id = referral_id).exists()
        if username_qs:
            raise serializers.ValidationError({'username': "Username Exist in Database"})
        if not link:
            raise serializers.ValidationError({'referral_id': "Invalid Referral Id"})
        if password != confirm_password:
            raise serializers.ValidationError({'password': 'Password must match'})
        user.set_password(password)
        user.save()

        # Link and Referal
        Link.objects.create(user = user)
        Wallet.objects.create(user = user)
        link = Link.objects.get(referral_id = referral_id)
        try:
            referral = Referral.objects.get(user = link.user)
            referral.add_child(user = user)
        except Referral.DoesNotExist:
            raise serializers.ValidationError('Referral with user = {} does not exist'.format(link.user))
        return user

# ########## User Login Serializer ##########    
# class UserLoginSerializer(serializers.Serializer):
#     username = serializers.CharField(required = True)
#     password = serializers.CharField(required = True, style = {'input_type': 'password'})
    
#     class Meta:
#         model = User
#         fields = ['username', 'password']

#     def validate(self, data):
#         user = authenticate(**data)
#         if user and user.is_active:
#             return user
#         raise serializers.ValidationError('Invalid credentials')