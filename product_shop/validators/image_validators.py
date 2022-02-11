from django.core.exceptions import ValidationError


def poster_size_validator(image):
    width = image.width
    height = image.height

    if width != 1300 and height != 400:
        raise ValidationError("Image must be the correct size 1300x400px !")


def image_size_validator(image):
    max_height = image.width

    if max_height > 250:
        raise ValidationError("Image to large")
    if max_height < 250:
        raise ValidationError("Image to small")
