from rest_framework import viewsets

from product_shop.pictures.models import PosterImage
from product_shop.pictures.serializers import PosterImageSerializer


class PosterImageViewSet(viewsets.ModelViewSet):
    queryset = PosterImage.objects.all()
    serializer_class = PosterImageSerializer
