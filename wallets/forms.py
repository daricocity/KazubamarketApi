from django import forms
from accounts.models import User
from .models import Transaction, Wallet

REG_PACKAGE = (
    ('', 'Select Package'),
    ('20', '$20 Package'),
    ('50', '$50 Package'),
    ('100', '$100 Package'),
)

class ReferPayForm(forms.Form):
    checkbalance = forms.MultipleChoiceField(widget = forms.CheckboxSelectMultiple,)

###############   FUND TRANSFER FORM   ############### 
class FundTransferForm(forms.ModelForm):
    wallet = forms.ModelChoiceField(queryset = Wallet.objects.all(), required = True)
    amount = forms.CharField(widget = forms.TextInput(attrs = { 'class':'form-control'}), required = True)
    reason = forms.CharField(widget = forms.Textarea(attrs = {'rows':'4', 'id':'reason', 'class':'form-control'}), required = True)
     
    class Meta:
        model = Transaction
        fields = ['wallets','amount','reason']
        
    def __init__(self, user, *args, **kwargs):
        super(FundTransferForm, self).__init__(*args, **kwargs)
        self.fields['wallets'].queryset = Wallet.objects.exclude(user = user)
        
###############   SUBSCRIPTION FORM   ############### 
class SubscriptionForm(forms.ModelForm):
    # wallets = forms.CharField(widget = forms.TextInput(attrs = { 'class':'form-control', 'readonly': True, 'style': 'background-color:#e5e5e5',}), required = True)
    wallet = forms.ModelChoiceField(queryset = Wallet.objects.filter(user = User.objects.get(admin = True)), required = True)
    amount = forms.CharField(widget = forms.TextInput(attrs = {'id':'amount', 'class':'form-control'}), required = True)
    reason = forms.CharField(widget = forms.Textarea(attrs = {'rows':'4', 'id':'reason', 'class':'form-control'}), required = True)      
    
    class Meta:
        model = Transaction
        fields = ['wallets','amount','reason']

###############   SUBSCRIPTION FORM   ############### 
class ActivationForm(forms.ModelForm):
    wallet = forms.ModelChoiceField(queryset = Wallet.objects.filter(user = User.objects.get(admin = True)), required = True)
    package = forms.ChoiceField(choices=REG_PACKAGE)
    amount = forms.CharField(widget = forms.TextInput(attrs = {'id':'amount', 'class':'form-control', 'readonly': True}), required = True)
    reason = forms.CharField(widget = forms.Textarea(attrs = {'rows':'4', 'id':'reason', 'class':'form-control'}), required = True)      
    
    class Meta:
        model = Transaction
        fields = ['wallets','amount','reason']