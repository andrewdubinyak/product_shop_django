from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from product_shop.products import views

app_name = 'products_api'
router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'catalog', views.CategoryViewSet)
router.register(r'sub-categories', views.SubCategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    re_path('^products-filter/(?P<category_name>.+)/$', views.ProductFilterViewSet.as_view())
]
