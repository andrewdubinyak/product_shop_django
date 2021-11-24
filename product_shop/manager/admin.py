from django.contrib import admin

from product_shop.manager.models import Liquidation, Order, Poster, PosterImage


class LiquidationAdmin(admin.ModelAdmin):
    model = Liquidation
    list_display = ('product', 'number', 'created_at')
    fields = ['product', 'number']


class OrderAdmin(admin.ModelAdmin):
    model = Order


class TabImageAdmin(admin.TabularInline):
    model = PosterImage
    list_display = ('image_tag',)
    readonly_fields = ['image_tag']


class PosterAdmin(admin.ModelAdmin):
    inlines = [TabImageAdmin]
    list_display = ('label',)
    fields = ['label', 'text']


admin.site.register(Liquidation, LiquidationAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Poster, PosterAdmin)
