from django.utils.text import slugify
from categorys.models import Category
from rest_framework import serializers
from products.models import Product, ProductImage
from accounts.api.serializers import UserDetailSerializer
from categorys.api.serializers import CategoryDetailSerializer

STOCK_STATUS = (
    ('In stock', 'In stock'),
    ('Out of stock', 'Out of stock'),
    ('On backorder', 'On backorder'),
)

########## PRODUCT DETAIL UPDATE SERIALIZER ##########
class ProductDetailUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = ['id','title','slug','description','regular_price', 'stock_status', 'quantity_stocked', 'delivery_location','category']
        
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title',instance.title)
        instance.slug = validated_data.get('slug',instance.slug)
        instance.description = validated_data.get('description',instance.description)
        instance.regular_price = validated_data.get('regular_price',instance.regular_price)
        instance.stock_status = validated_data.get('stock_status',instance.stock_status)
        instance.quantity_stocked = validated_data.get('quantity_stocked',instance.quantity_stocked)
        instance.delivery_location = validated_data.get('delivery_location',instance.delivery_location)
        instance.category = validated_data.get('category',instance.category)
        instance = super().update(instance, validated_data)
        return instance

########## PRODUCT LIST SERIALIZER ##########
class ProductListSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    images = serializers.SerializerMethodField()
    # category = CategoryDetailSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'description', 'regular_price', 'stock_status', 'quantity_stocked', 'delivery_location', 'category', 'images', 'user']

    def get_images(self, obj):
        return [product_image.image.url for product_image in obj.productimage_set.all()]

########## PRODUCT USER LIST SERIALIZER ##########
class ProductUserListSerializer(serializers.ModelSerializer):
    category = CategoryDetailSerializer(read_only=True)
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'description', 'regular_price', 'stock_status', 'quantity_stocked', 'delivery_location', 'category', 'images']

    def get_images(self, obj):
        return [product_image.image.url for product_image in obj.productimage_set.all()]
   
########## PRODUCT SERIALIZER ##########
class CategoryFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):

    def get_queryset(self):
        request = self.context.get('request', None)
        queryset = super(CategoryFilteredPrimaryKeyRelatedField, self).get_queryset()
        if not request or not queryset:
            return None
        return queryset.filter(user=request.user)

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('image',)

class ProductSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault(), read_only = False)
    slug = serializers.SerializerMethodField(read_only=True)
    category = CategoryFilteredPrimaryKeyRelatedField(queryset=Category.objects, many=False)
    stock_status = serializers.ChoiceField(choices=STOCK_STATUS)
    images = ProductImageSerializer(source='productimage_set', many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['user', 'title', 'slug', 'description', 'regular_price', 'category', 'stock_status', 'quantity_stocked', 'delivery_location', 'images']

    def get_slug(self, instance):
        return slugify(instance.title)
        
    def get_user(self, obj):
        return obj.request.user
        
    def create(self, validated_data):
        images_data = self.context.get('view').request.FILES
        product = Product.objects.create(**validated_data)
        for image_data in images_data.values():
            ProductImage.objects.create(product=product, image=image_data)
        return product
