from django.contrib import admin

from product_shop.manager.models import Liquidation


class LiquidationAdmin(admin.ModelAdmin):
    model = Liquidation
    list_display = ('product', 'number', 'created_at')
    fields = ['product', 'number']


admin.site.register(Liquidation, LiquidationAdmin)
