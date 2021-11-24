from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.safestring import mark_safe

from product_shop.accounts.models import User
from product_shop.products.models import Product


class Liquidation(models.Model):
    number = models.DecimalField(max_digits=20, decimal_places=2)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL, related_name='liquidations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} {}".format(self.number, self.product)


@receiver(post_save, sender=Liquidation, dispatch_uid="update_balance_count")
def update_balance(instance, created, **kwargs):
    if created:
        instance.product.amount = instance.product.amount - instance.number
        if instance.product.amount <= 0:
            instance.product.amount = 0
            instance.product.active = False
            instance.product.save()
        instance.product.save()


class Order(models.Model):
    STATUS = (
        (1, 'COMPLETE'),
        (2, 'CANCELED'),
        (3, 'IN PROGRESS')
    )
    PAYMENT = (
        (1, 'CASH'),
        (2, 'ONLINE')
    )

    customer = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField(Product)
    address = models.CharField(max_length=255)
    total_price = models.CharField(max_length=255)
    payment_method = models.IntegerField(choices=PAYMENT)
    is_paid = models.BooleanField(default=False)
    status = models.IntegerField(choices=STATUS)
    transaction_id = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Poster(models.Model):
    label = models.CharField(max_length=255)
    text = models.TextField(null=True, blank=True)


class PosterImage(models.Model):
    poster = models.ForeignKey('Poster', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/')

    def image_tag(self):
        return mark_safe('<img src="{}" width="300" height="200" />'.format(self.image.url))

    image_tag.short_description = 'Image Preview'
