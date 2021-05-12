import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from product_shop.accounts.managers.user_manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=500, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    can_impersonate = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

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
