import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from product_shop.accounts.managers.user_manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=500, blank=True, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    USER_TYPE_CHOICES = (
        (1, 'courier'),
        (2, 'buyer'),
        (3, 'manager'),
    )

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'

    objects = UserManager()

    class Meta:
        app_label = 'accounts'

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.lower()
        if not self.password:
            self.password = str(uuid.uuid4()).replace('-', '')
        super(User, self).save(*args, **kwargs)


class OTPLogin(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_phone = models.IntegerField(blank=False)
    is_verified = models.BooleanField(blank=False, default=False)
    counter = models.IntegerField(default=0, blank=False)

    def __str__(self):
        return str(self.mobile_phone)


class UserAddress(models.Model):
    address = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_addresses')
