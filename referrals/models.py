import uuid
from django.db import models
from django.urls import reverse
from treebeard.mp_tree import MP_Node
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, pre_save
from KazubamarketApi.utils import unique_referral_id_generator

User = get_user_model()

###############  LINK QUERYSET  ###############
class LinkQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active = True)
 
###############  LINK MANAGER  ###############   
class LinkManager(models.Manager):
    def get_queryset(self):
        return LinkQuerySet(self.model, using = self._db)

    def all(self):
        return self.get_queryset().active()

###############   LINK   ###############
class Link(models.Model):
    user = models.OneToOneField(User,  on_delete = models.CASCADE)
    referral_id = models.CharField(max_length = 20, blank = True)
    token = models.UUIDField(default = uuid.uuid4, editable = False, unique = True)
    active = models.BooleanField(default = True)
    
    objects = LinkManager()

    def __str__(self):
        return str(self.referral_id)
    
def link_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.referral_id:
        instance.referral_id = unique_referral_id_generator(instance)
pre_save.connect(link_pre_save_receiver, sender = Link)

###############   REFERRAL   ###############
class Referral(MP_Node):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    node_order_by = ['user']
    path = models.CharField(max_length=99000000)
    created = models.DateTimeField(auto_now_add = True)
    has_paid_activation = models.BooleanField(default = False)
    package = models.CharField(max_length = 100, blank = True)
    activated_on = models.DateTimeField(auto_now_add = True)
    steplen = 5

    class Meta:
        db_table = 'referral'

    def get_absolute_url(self):
        return reverse('referrals:referral_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.user.username
    
    def get_referral_ids(self):
        user_in = Link.objects.get(user = self.user).referral_id
        return user_in
    
    def get_absolute_user_referral_url(self):
        return reverse("referrals:referral_users_detail", kwargs={"slug": self.user})
