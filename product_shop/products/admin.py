from django.contrib import admin
from django.db import models
from django.forms import NumberInput

from product_shop.products.models import Product, Category, Characteristic, Image, SubCategory, ProductImage


class TabImageAdmin(admin.StackedInline):
    model = ProductImage
    extra = 0
    readonly_fields = ['image_tag']


class ProductAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.IntegerField: {'widget': NumberInput(attrs={'size': '40'})},
    }
    search_fields = ['name', 'barcode']
    list_display = ['name', 'barcode', 'category', 'amount', 'type', 'price', 'active']
    fields = ['name', 'category', 'sub_category', 'barcode', 'amount', 'type', 'price', 'active', 'characteristic']
    list_filter = ['type', 'category', 'active']
    inlines = [TabImageAdmin]


class SubCategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ('name', 'category')
    list_display = ('name', 'category')
    fields = ['name', 'category']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_icon']
    readonly_fields = ['get_image']

    def get_image(self, obj):
        return obj.image_tag()

    def get_icon(self, obj):
        return obj.icon_tag()

    get_icon.short_description = 'Icon'
    get_image.short_description = 'Image preview'


class CharacteristicAdmin(admin.ModelAdmin):
    list_display = ['brand', 'packaging', 'manufacturer']


class ImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_tag')
    readonly_fields = ['image_tag', ]
    fields = ['name', 'image', 'image_tag']


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Characteristic, CharacteristicAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
