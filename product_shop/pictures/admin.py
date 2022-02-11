from django.contrib import admin

from product_shop.pictures.models import PosterImage, Poster


class TabImageAdmin(admin.TabularInline):
    model = PosterImage
    list_display = ('image_tag',)
    readonly_fields = ['image_tag']


class PosterAdmin(admin.ModelAdmin):
    inlines = [TabImageAdmin]
    list_display = ('label',)
    fields = ['label', 'text']


admin.site.register(Poster, PosterAdmin)
