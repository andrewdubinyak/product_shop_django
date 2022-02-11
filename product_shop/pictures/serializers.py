from rest_framework import serializers

from product_shop.pictures.models import PosterImage


class PosterImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PosterImage
        fields = '__all__'
