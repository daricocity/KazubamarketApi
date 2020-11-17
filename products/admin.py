from django.contrib import admin
from .models import Product, ProductImage
from django.core.paginator import Paginator

# Register your models here.
########## PRODUCT ADMIN ##########
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'stock', 'price', 'category_display', 'featured', 'date_published']
    search_fields = ['title', 'regular_price','category']
    list_filter = ['category','stock_status','timestamp']
    list_display_links = ['name', 'category_display']
    list_editable = ['featured']
    list_per_page = 10
    paginator = Paginator

    class Meta:
        model = Product

    def date_published(self, obj):
        return obj.timestamp

    def name(self, obj):
        return obj.title

    def price(self, obj):
        return "\u20A6{:,.2f}".format(obj.regular_price)

    def stock(self, obj):
        return obj.stock_status

    def category_display(self, obj):
        return obj.category
admin.site.register(Product, ProductAdmin)

########## PRODUCT IMAGE ADMIN ##########
class ProductImageAdmin(admin.ModelAdmin):
    search_fields = ['id', 'product']
    list_per_page = 50
    paginator = Paginator

    class Meta:
        model = ProductImage
admin.site.register(ProductImage, ProductImageAdmin)
