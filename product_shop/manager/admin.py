from django.contrib import admin

from product_shop.manager.models import Liquidation, Order


class LiquidationAdmin(admin.ModelAdmin):
    model = Liquidation
    list_display = ('product', 'number', 'created_at')
    fields = ['product', 'number']


class OrderAdmin(admin.ModelAdmin):
    model = Order


admin.site.register(Liquidation, LiquidationAdmin)
admin.site.register(Order, OrderAdmin)
