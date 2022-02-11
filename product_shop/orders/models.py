from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

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
        ('complete', 'COMPLETE'),
        ('canceled', 'CANCELED'),
        ('in_progress', 'IN PROGRESS')
    )
    PAYMENT = (
        ('cash', 'CASH'),
        ('online', 'ONLINE')
    )

    customer = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name='orders')
    courier = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='courier_orders')
    address = models.CharField(max_length=255)
    total_price = models.FloatField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, choices=PAYMENT)
    is_paid = models.BooleanField(default=False)
    status = models.CharField(null=True, blank=True, max_length=50, choices=STATUS)
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.customer)


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.CASCADE, related_name='order_products')
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE, related_name='product_orders')
    quantity = models.IntegerField()
    sub_total = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.product.name


@receiver(post_save, sender=OrderProduct, dispatch_uid="update_balance_count")
def update_product_amount(instance, created, **kwargs):
    if created:
        instance.product.amount = instance.product.amount - int(instance.quantity)
        instance.product.save()
