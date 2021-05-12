from rest_framework import serializers
from product_shop.products.models import Product, Category, Characteristic, Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    image = ImageSerializer(read_only=True)

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
    image = ImageSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = '__all__'
