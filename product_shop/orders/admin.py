from django.contrib import admin

from product_shop.orders.models import Liquidation, Order, OrderProduct


class LiquidationAdmin(admin.ModelAdmin):
    model = Liquidation
    list_display = ('product', 'number', 'created_at')
    fields = ['product', 'number']


class InlineProducts(admin.TabularInline):
    model = OrderProduct


class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ('customer', 'status', 'total_price', 'address')
    inlines = [InlineProducts]


admin.site.register(Liquidation, LiquidationAdmin)
admin.site.register(Order, OrderAdmin)
