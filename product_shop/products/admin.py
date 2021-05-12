from django.contrib import admin
from product_shop.products.models import Product, Category, Characteristic, Image, SubCategory


class TabImageAdmin(admin.TabularInline):
    model = Product.image.through
    list_display = ['name', 'image']


class ProductAdmin(admin.ModelAdmin):
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
    list_display = ['name']


class CharacteristicAdmin(admin.ModelAdmin):
    list_display = ['brand', 'packaging', 'manufacturer']


class ImageAdmin(admin.ModelAdmin):
    list_display = ['name', 'image']


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Characteristic, CharacteristicAdmin)
admin.site.register(Image)
admin.site.register(SubCategory, SubCategoryAdmin)
