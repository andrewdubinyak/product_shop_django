def get_total_price(products):
    return sum(item.get('product').price * int(item.get('quantity')) for item in products)


def get_sub_total(products):
    return [item.get('product').price * int(item.get('quantity')) for item in products]


def get_total_cart_price(products):
    return sum(item.get('price_per_unit') * int(item.get('quantity')) for item in products)
