from django.urls import path, include
from rest_framework.routers import DefaultRouter

from product_shop.orders import views

app_name = 'products_api'
router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('cart/', views.CartView.as_view(), name='all_cart_items'),
    path('cart/<int:id>', views.CartView.as_view(), name='add_to_card'),
    path('orders/', views.OrderView.as_view(), name='all_orders'),
    path('orders/create', views.OrderView.as_view(), name='create_order'),
    path('orders/<int:id>/assign', views.OrderAssignView.as_view(), name='create_order'),
    path('orders/<int:id>', views.OrderView.as_view(), name='order_detail'),
]
