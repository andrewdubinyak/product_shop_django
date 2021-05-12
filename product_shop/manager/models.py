from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

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
