from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
User = get_user_model()


######### USER ADMIN ##########
class UserAdmin(BaseUserAdmin):

    class Meta:
        model = User

    def date_registered(self, obj):
        return obj.timestamp

    def Last_subscrption_date(self, obj):
        return obj.subscription_date
        # return obj.subcripted

    list_display = ('username', 'email', 'admin', 'date_registered', 'Last_subscrption_date')
    list_filter = ('is_active', 'timestamp')
    fieldsets = (
        ('Authentication', {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'full_name', 'phone_number', 'occupation', 'address', 'name_block')}),
        ('Bank account Details', {'fields': ('bank_account_name', 'bank_account_number', 'bank_name',)}),
        ('Permissions', {'fields': ('admin', 'staff', 'is_active', 'is_subscribe', 'subscription_date')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2',)}
         ),
    )
    search_fields = ('username', 'email', 'full_name',)
    ordering = ('username',)
    filter_horizontal = ()
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.site_header = 'Kazubamarket Administration'
admin.site.index_title = 'Admin'
admin.site.site_title = 'Kazubamarket'