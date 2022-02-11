from django.db import models
from django.utils.safestring import mark_safe

from product_shop.validators.image_validators import poster_size_validator


class Poster(models.Model):
    label = models.CharField(max_length=255)
    text = models.TextField(null=True, blank=True)


class PosterImage(models.Model):
    poster = models.ForeignKey('Poster', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/', validators=[poster_size_validator])

    def image_tag(self):
        return mark_safe('<img src="{}" width="300" height="200" />'.format(self.image.url))

    image_tag.short_description = 'Image Preview'
