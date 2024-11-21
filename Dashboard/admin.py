from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserForm
from .models import CustomUser, Transaction, WebsiteConfiguration

CustomUser = get_user_model()

class CustomUserAdmin(UserAdmin):
    form = CustomUserForm
    add_form = CustomUserForm  # Use the same form for creating users
    
    # Specify the fields that should be visible in the admin interface
    list_display = ['username', 'balance', 'email', 'nin', 'is_active', 'is_staff', 'get_bank_account']
    search_fields = ['username', 'email']
    ordering = ['username']
    
    # Fields for add and change user forms
    fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2', 'balance', 'bank_account', 'nin')}),  # Add nin to fieldsets, remove first_name and last_name
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),  # permissions
        ('Important dates', {'fields': ('last_login', 'date_joined')}),           # important date fields
    )
    
    # Fields for the 'Add User' form
    add_fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2', 'balance', 'bank_account', 'nin')}),  # Add nin to the 'Add User' form
    )
    
    # Exclude any fields you do not want to display in the admin form (like 'usable_password' if it exists)
    exclude = ['usable_password']

    # Add a custom method to display the bank account information in the list view
    def get_bank_account(self, obj):
        """ Display bank account information in the list view """
        if obj.bank_account and 'accounts' in obj.bank_account:
            accounts = obj.bank_account['accounts']
            if accounts:
                # Return a formatted string for the first account in the list
                account_info = accounts[0]  # You can adjust this if you want to show all accounts
                return f"{account_info.get('bankName', 'No Bank Name')} - {account_info.get('accountName', 'No Account Name')} - {account_info.get('accountNumber', 'No Account Number')}"
        return 'No Bank Account'
    
    # Set the method name as the column header in the list display
    get_bank_account.short_description = 'Bank Account'


@admin.register(WebsiteConfiguration)
class WebsiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ('base_url', 'auth_token')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Transaction)