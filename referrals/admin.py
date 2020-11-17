from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from .models import Link, Referral

@admin.register(Referral)
class MultiLevelReferralAdmin(TreeAdmin):
    form = movenodeform_factory(Referral)

class LinkAdmin(admin.ModelAdmin):
    list_display = ['user', 'referral_id', 'token']
    readonly_fields = ['token']
admin.site.register(Link, LinkAdmin)