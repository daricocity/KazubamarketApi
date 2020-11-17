from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
########## USER QUERYSET ##########
class UserQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active = True)

########## USER MANAGER ##########
class UserManager(BaseUserManager):
    def create_user(self, email, username, full_name = None, password = None, is_active = True, is_staff = False, is_admin = False, is_subscribe = False):
        if not username:
            raise ValueError("User must have username")
        if not email:
            raise ValueError("User must have an email address")
        if not password:
            raise ValueError("User must have a password")
        user_obj = self.model(email = self.normalize_email(email), username = username, full_name = full_name)
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.subscribe = is_subscribe
        user_obj.save(using = self._db)
        return user_obj

    def create_staffuser(self, email, username, full_name = None, password = None):
        user = self.create_user(email, username = username, full_name = full_name, password = password, is_staff = True)
        return user

    def create_superuser(self, email, username, full_name = None, password = None):
        user = self.create_user(email, username = username, full_name = full_name, password = password, is_staff = True, is_admin = True)
        return user

########## USER MODEL ##########
class User(AbstractBaseUser):
    username = models.CharField(unique = True, max_length = 255, blank = True, null = True)
    email = models.EmailField(max_length = 255, blank = True, null = True)
    full_name = models.CharField(max_length = 255, blank = True, null = True)
    occupation = models.CharField(max_length = 200, blank = True, null = True)
    phone_number = models.CharField(max_length = 20, blank = True, null = True)
    address = models.TextField(max_length = 300, blank = True, null = True)
    name_block = models.CharField(max_length = 255, blank = True, null = True)
    bank_account_name = models.CharField(max_length = 50, blank = True, null = True)
    bank_account_number = models.CharField(max_length = 50, blank = True, null = True)
    bank_name = models.CharField(max_length = 50, blank = True, null = True)
    is_active = models.BooleanField(default = True)
    staff = models.BooleanField(default = False)
    admin = models.BooleanField(default = False)
    is_subscribe = models.BooleanField(default = False)
    subscription_date = models.CharField(max_length = 50, blank = True)
    timestamp = models.DateTimeField(auto_now_add = True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username

    def get_full_name(self):
        if self.full_name:
            return self.full_name
        return self.username

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        if self.admin:
            return True
        return False

    def has_module_perms(self, app_label):
        if self.admin:
            return True
        return False

    def is_staff(self):
        if self.is_admin:
            return True
        return self.staff

    def is_admin(self):
        return self.admin

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)