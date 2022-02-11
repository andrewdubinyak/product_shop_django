from rest_framework import serializers
from product_shop.products.models import Product, Category, Characteristic, SubCategory, ProductImage


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image', 'is_default']


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['name', 'slug']


class CategorySerializer(serializers.ModelSerializer):
    sub_categories = SubCategorySerializer(read_only=True, many=True)

    class Meta:
        model = Category
        fields = '__all__'


class CharacteristicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Characteristic
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    characteristic = CharacteristicSerializer(read_only=True)
    product_images = ImageSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = '__all__'


class ProductFilterSerializer(serializers.ModelSerializer):
    product_images = ImageSerializer(read_only=True, many=True)

    class Meta:
        depth = 1
        model = Product
        fields = '__all__'
