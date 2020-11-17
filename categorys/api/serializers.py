from django.utils.text import slugify
from categorys.models import Category
from rest_framework import serializers
from accounts.api.serializers import UserDetailSerializer

########## CATEGORY USER SERIALIZER ##########
class CategoryListSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'description', 'user']

########## Category Detail Update Serializer ##########
class CategoryDetailUpdateSerializer(serializers.ModelSerializer):
    slug = serializers.SerializerMethodField(read_only=True)

    def get_slug(self, instance):
        return slugify(instance.title)
    
    class Meta:
        model = Category
        fields = ['id','title','slug','description',]
        
    def update(self, instance, validated_data):
        instance.slug = validated_data.get(instance.slug)
        instance.title = validated_data.get('title',instance.title)
        instance.description = validated_data.get('description',instance.description)
        instance = super().update(instance, validated_data)
        return instance

########## CATEGORY DETAIL SERIALIZER ##########   
class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id']

########## CATEGORY USER SERIALIZER ##########
class CategoryUserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'description']

########## CATEGORY SERIALIZER ##########
class CategorySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    slug = serializers.SerializerMethodField(read_only=True)

    def get_slug(self, instance):
        return slugify(instance.title)

    class Meta:
        model = Category
        fields = ['user', 'title', 'slug', 'description']
        
    def get_user(self, obj):
        return obj.request.user