from django.urls import path, include
from rest_framework.routers import DefaultRouter

from product_shop.pictures import views

app_name = 'products_api'
router = DefaultRouter()

router.register(r'posters', views.PosterImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
