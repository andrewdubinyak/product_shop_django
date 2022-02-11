import redis
from django.conf import settings

from product_shop.products.models import Product

redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT,
                                   charset="utf-8", decode_responses=True)


def add_to_cart(session_key, data):
    redis_instance.hset(session_key, data['product_id'], data['quantity'])
    redis_instance.expire(session_key, 60 * 60 * 24 * 2)


def remove_from_cart(session_key, product_id):
    redis_instance.hdel(session_key, product_id)


def get_all_cart(session_key):
    redis_data = redis_instance.hgetall(session_key)
    cart_items = []
    for key, value in redis_data.items():
        # cart_items.append(dict({'product_id': int(key), 'count': int(value)}))
        product = Product.objects.filter(id=int(key)).first()
        cart_items.append({'id': product.id,
                           'name': product.name,
                           'quantity': int(value),
                           'price_per_unit': product.price,
                           'price': int(value) * product.price})
    # products = Product.objects.filter(id__in=(x['product_id'] for x in cart_items)).all()

    return cart_items
