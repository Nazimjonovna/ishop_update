from rest_framework import serializers
from .models import *

class CreateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name',]


class CreateSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['name',]

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ('id', 'name')


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'subcategories')


class ProductInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInfo
        fields = ('id', 'language', 'name', 'about', 'description', 'subcategory', 'model')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'color_key', 'image')


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    product_info = ProductInfoSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'quantity', 'cost', 'time', 'prosent', 'postavshik', 'admin', 'tasdiq', 'category', 'product_info', 'images')

    def get_category(self, obj):
        subcategory = obj.productinfo_set.first().subcategory
        category = subcategory.category
        return CategorySerializer(category).data
    

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'