from django.db import models
from django.conf import settings
from products.models import Product
from django.db.models.signals import pre_save
from KazubamarketApi.utils import unique_order_id_generator

# Create your models here.
User = settings.AUTH_USER_MODEL

########## ORDER QUERYSET ##########
class OrderQuerySet(models.QuerySet):
    def active(self):
        return self.filter(active = True)

########## ORDER MANAGER ##########
class OrderManager(models.Manager):
    def get_queryset(self):
        return OrderQuerySet(self.model, using = self._db)

    def all(self):
        return self.get_queryset().active()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id = id)
        if qs.count() == 1:
            return qs.first()
        return None

########## ORDER MODEL ##########
class Order(models.Model):
    user = models.ForeignKey(User, null = True, blank = True, on_delete = models.CASCADE)
    order_id = models.CharField(max_length = 120, blank = True)
    total = models.CharField(max_length = 120, null = True, blank = True)
    payment_method = models.CharField(max_length = 100, null = True, blank = True)
    timestamp = models.DateTimeField(auto_now_add = True)
    active = models.BooleanField(default = True)

    def __str__(self):
        return self.order_id

    objects = OrderManager()

def order_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)
pre_save.connect(order_pre_save_receiver, sender = Order)

########## CART QUERYSET ##########
class CartQuerySet(models.QuerySet):
    def active(self):
        return self.filter(active = True)

########## CART MANAGER ##########
class CartManager(models.Manager):
    def get_queryset(self):
        return CartQuerySet(self.model, using = self._db)

    def all(self):
        return self.get_queryset().active()

########## CART MODEL ##########
class Cart(models.Model):
	user = models.ForeignKey(User, null = True, blank = True, on_delete = models.CASCADE)
	order = models.ForeignKey(Order, null = True, blank = True, on_delete = models.CASCADE)
	product = models.ForeignKey(Product, blank = True, null = True, on_delete = models.CASCADE)
	quantity = models.PositiveIntegerField()
	line_total = models.DecimalField(max_digits = 10, decimal_places = 2, default = 00.00)
	timestamp = models.DateTimeField(auto_now_add = True)
	active = models.BooleanField(default = True)

	objects = CartManager()

	def __str__(self):
		return self.order.order_id + ' Order'