from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserForm
from .models import CustomUser, Transaction

CustomUser = get_user_model()

class CustomUserAdmin(UserAdmin):
    form = CustomUserForm
    add_form = CustomUserForm  # Use the same form for creating users
    
    # Specify the fields that should be visible in the admin interface
    list_display = ['username', 'balance', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']
    search_fields = ['username', 'email']
    ordering = ['username']
    
    # Fields for add and change user forms
    fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2', 'balance')}),  # basic fields for user creation
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),     # personal info
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),  # permissions, including 'is_active' and 'is_staff'
        ('Important dates', {'fields': ('last_login', 'date_joined')}),           # important date fields
    )
    
    # Fields for the 'Add User' form
    add_fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2', 'balance')}),  # same as change form, but without personal info
    )
    
    # Exclude any fields you do not want to display in the admin form (like 'usable_password' if it exists)
    exclude = ['usable_password']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Transaction)
