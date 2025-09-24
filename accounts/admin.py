# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = CustomUser

    list_display = ['username', 'role', 'is_staff', 'is_active']

    # Fields shown in admin when editing a user
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Role Info', {'fields': ('role',)}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Fields shown when creating a new user in admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'role', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

    search_fields = ('username',)
    ordering = ('username',)


admin.site.register(CustomUser, CustomUserAdmin)
