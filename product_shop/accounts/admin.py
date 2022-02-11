from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from product_shop.accounts.models import User, UserAddress


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserAddressInline(admin.TabularInline):
    model = UserAddress
    extra = 0
    fields = ['address']


class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    list_display = ('email', 'phone_number')

    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name', 'phone_number', 'user_type')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'phone_number', 'password', 'first_name', 'last_name', 'user_type', 'is_superuser', 'is_staff',
                'is_active')}
         ),
    )

    filter_horizontal = ()
    ordering = ('email',)
    inlines = [UserAddressInline]


admin.site.register(User, CustomUserAdmin)
