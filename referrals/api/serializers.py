import datetime
from accounts.models import User
from django.utils import timezone
from datetime import timedelta, date
from rest_framework import serializers
from referrals.models import Referral, Link

########## LINK SERIALIZER ##########
class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ['user', 'referral_id']

########## REFERRAL SERIALIZER ##########
class ReferralSerializer(serializers.ModelSerializer):
    downline_name = serializers.SerializerMethodField()
    referral_id = serializers.SerializerMethodField()
    date_activated = serializers.SerializerMethodField()
    referral_parent = serializers.SerializerMethodField()

    class Meta:
        model = Referral
        fields = ['id', 'downline_name', 'referral_id', 'date_activated', 'package', 'referral_parent']

    def get_referral_id(self, obj):
        return Link.objects.get(user = obj.user).referral_id

    def get_downline_name(self, obj):
        return obj.user.username
    
    def get_date_activated(self, obj):
        return obj.activated_on

    def get_referral_parent(self, obj):
        return obj.activated_on
        # return obj.get_referral_ids()

    def get_object(self):
        user = self.context['request'].user
        return user
        