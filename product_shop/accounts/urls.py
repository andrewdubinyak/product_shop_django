from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from product_shop.accounts.views import RegisterView, UserProfileView, OTPLoginView

urlpatterns = [
    path('login/', obtain_jwt_token, name='get_token'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('phone-login/<phone>', OTPLoginView.as_view(), name='phone_confirmation'),
    # url(r'phone-login', include('rest_pyotp.routers')),
    # url(r'^phone_login/', include('phone_login.urls')),
    # path('sms-login/', SmsLoginView.as_view(), name='phone_confirmation')
]
