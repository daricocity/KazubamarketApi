import os
import random
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.conf import settings
from accounts.models import User
from categorys.models import Category
from django.db.models.signals import pre_save
from django.utils.safestring import mark_safe
from KazubamarketApi.utils import unique_slug_generator

STOCK_STATUS = (
    ('In stock', 'In stock'),
    ('Out of stock', 'Out of stock'),
    ('On backorder', 'On backorder'),
)

# Create your models here.
###############   FILENAME    ###############
def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_product_image_path(instance, filename):
    new_filename = random.randint(1,2039489097)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename = new_filename, ext = ext)
    return "products/{final_filename}".format(final_filename = final_filename)

########## PRODUCT QUERYSET ##########
class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active = True)

    def featured(self):
        return self.filter(featured = True, active = True)

    def search(self, query):
        lookups = (
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(regular_price__icontains=query) |
            Q(tag__title__icontains=query) |
            Q(category__title__icontains=query)
        )
        return self.filter(lookups).distinct()

########## PRODUCT MANAGER ##########
class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using = self._db)

    def all(self):
        return self.get_queryset().active()

    # Get Only the featured Objects that is true in Database
    def featured(self):
        return self.get_queryset().filter(featured = True)

    # Get Individual Objects in Database
    def get_by_id(self, id):
        qs = self.get_queryset().filter(id = id)
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset().active().search(query)

########## PRODUCT MODEL ##########
class Product(models.Model):
    user = models.ForeignKey(User, null = True, blank = True, on_delete = models.CASCADE)
    title = models.CharField(blank = True, max_length = 120, help_text = 'Enter the name of the product')
    slug = models.SlugField(blank = True, unique = True, help_text = 'Leave blank for the system to generate')
    description = models.TextField(blank = True, help_text = 'Enter the product full desciption')
    regular_price = models.DecimalField(decimal_places = 2, max_digits = 20, default = 39.99, help_text = 'Enter the product prize')
    sales_price = models.DecimalField(decimal_places = 2, max_digits = 20, null = True, blank = True, help_text = 'sales prize shoud be less than regular prize')
    category = models.ForeignKey(Category, blank = True, null = True, help_text = 'Select product category', on_delete = models.CASCADE)
    stock_status = models.CharField(blank = True, max_length = 120, choices = STOCK_STATUS, help_text = 'Select product stock status')
    quantity_stocked = models.SmallIntegerField(default = 0, help_text = 'Enter the quantity of product in stock')
    delivery_location = models.TextField(max_length = 300, blank = True, null = True)
    featured = models.BooleanField(default = False)
    date_to_featured = models.CharField(max_length = 50, blank = True)
    active = models.BooleanField(default = True)
    timestamp = models.DateTimeField(auto_now_add = True)

    objects = ProductManager()

    def get_category(self):
        qs = Category.objects.filter(product__title = self.title)
        if qs.count() >= 1:
            data = qs.first()
            return data
        return None

    def __str__(self):
        return self.title

def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
pre_save.connect(product_pre_save_receiver, sender = Product)

########## PRODUCT IMAGE QUERYSET  ##########
class ProductImageQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active = True)

########## PRODUCT IMAGE MANAGER  ##########
class ProductImageManager(models.Manager):
    def get_queryset(self):
        return ProductImageQuerySet(self.model, using = self._db)

    def all(self):
        return self.get_queryset().active()

########## PRODUCT IMAGE MODEL  ##########
class ProductImage(models.Model):
    product = models.ForeignKey(Product, null = True, blank = True, on_delete = models.CASCADE)
    image = models.ImageField(upload_to = upload_product_image_path, null = True, blank = True, help_text = 'Upload image file size of 300x300')
    active = models.BooleanField(default = True) 
    
    objects = ProductImageManager()
    
    def __str__(self):
        return self.product.title + ' Image'