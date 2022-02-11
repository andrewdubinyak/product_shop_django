from rest_framework import serializers
from django.db import transaction
from rest_framework.exceptions import APIException

from product_shop.orders.models import Order, OrderProduct
from product_shop.services import order_service


class OrderProductSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.FloatField(source='product.price', read_only=True)

    class Meta:
        model = OrderProduct
        fields = ('product', 'product_name', 'quantity', 'product_price', 'sub_total')


class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    payment_method = serializers.CharField(required=False)
    order_products = OrderProductSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = ('id', 'customer', 'courier', 'address', 'payment_method', 'total_price', 'is_paid', 'status',
                  'transaction_id', 'created_at', 'updated_at', 'order_products')

    def create(self, validated_data):
        print(validated_data)
        customer = self.context['request'].user
        cart = validated_data.get('order_products')
        address = validated_data.get('address')
        payment_method = validated_data.get('payment_method')
        total_price = order_service.get_total_price(cart)
        sub_total_price = order_service.get_sub_total(cart)

        try:
            with transaction.atomic():
                order = Order.objects.create(address=address, payment_method=payment_method,
                                             customer=customer, total_price=total_price,
                                             status='in_progress', transaction_id='123123')

                OrderProduct.objects.bulk_create([OrderProduct(
                    **{'order': order, 'product': item.get('product'), 'quantity': item.get('quantity'),
                       'sub_total': price}) for item, price in zip(cart, sub_total_price)])

        except Exception:
            error_message = 'There was a problem creating the order'
            raise APIException(detail=error_message)

        return order
