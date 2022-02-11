from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('__debug__/', include('debug_toolbar.urls')),
                  path('admin/', admin.site.urls),
                  path('api/', include('product_shop.products.urls', namespace='products_api')),
                  path('api-cart/', include('product_shop.orders.urls', namespace='carts_api')),
                  path('api-pictures/', include('product_shop.pictures.urls', namespace='pictures_api')),
                  path('api-auth/', include('product_shop.accounts.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
