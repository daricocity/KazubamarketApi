from django.db import models
from django.urls import reverse
from django.conf import settings
from django.db.models.signals import pre_save
from KazubamarketApi.utils import unique_slug_generator

User = settings.AUTH_USER_MODEL

# Create your models here.
########## CATEGORY QUERYSET ##########
class CategoryQuerySet(models.QuerySet):
    def active(self):
        return self.filter(active = True)

########## CATEGORY MANAGER ##########
class CategoryManager(models.Manager):
    def get_queryset(self):
        return CategoryQuerySet(self.model, using = self._db)

    def all(self):
        return self.get_queryset().active()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id = id)
        if qs.count() == 1:
            return qs.first()
        return None

########## CATEGORY MODEL ##########
class Category(models.Model):
    user = models.ForeignKey(User, null = True, blank = True, on_delete = models.CASCADE)
    title = models.CharField(blank = True, max_length = 120, help_text = 'Enter the name of the category')
    slug = models.SlugField(blank = True, unique = True, help_text = 'Leave blank for the system to generate')
    description = models.TextField(blank = True, help_text = 'Enter the category full desciption')
    active = models.BooleanField(default = True)
    timestamp = models.DateTimeField(auto_now_add = True)

    objects = CategoryManager()

    def __str__(self):
        return self.title

def category_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
pre_save.connect(category_pre_save_receiver, sender = Category)
