from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserForm
from django.db import models
from django import forms
from .models import CustomUser, MonnifyTransaction, BankTransfer, FakeLoginAttempt, Notification, Transaction, WebsiteConfiguration, BuyAirtime, BuyData, TVService, ElectricityBill, WaecPinGenerator, JambRegistration
import json

class CustomUserAdmin(UserAdmin):
    form = CustomUserForm
    add_form = CustomUserForm

    list_display = ['username', 'balance', 'email', 'nin', 'bvn', 'is_active', 'is_staff', 'get_bank_account', 'has_filled_fund_form']
    search_fields = ['username', 'email']
    ordering = ['username']

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # if obj and isinstance(obj.bank_account, dict):
        #     obj.bank_account = json.dumps(obj.bank_account, indent=2)
        return form

    fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2', 'balance', 'bonus', 'bank_account', 'nin', 'bvn', 'referred_by', 'referral_bonus', 'first_deposit_reward_given','failed_attempts', 'has_filled_fund_form')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2', 'balance', 'bank_account', 'nin', 'bvn')}),
    )

    exclude = ['usable_password']

    def get_bank_account(self, obj):
        if obj.bank_account and 'accounts' in obj.bank_account:
            accounts = obj.bank_account['accounts']
            if accounts:
                account_info = accounts[0]
                return f"{account_info.get('bankName', 'No Bank Name')} - {account_info.get('accountName', 'No Account Name')} - {account_info.get('accountNumber', 'No Account Number')}"
        return 'No Bank Account'

    get_bank_account.short_description = 'Bank Account'

@admin.register(MonnifyTransaction)
class MonnifyTransactionAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'amount', 'payment_reference', 'monnify_transaction_reference',
        'bank_code', 'account_number', 'transaction_type',  # 👈 Added
        'status', 'currency', 'date'
    )
    search_fields = (
        'user__username', 'payment_reference', 'monnify_transaction_reference', 'account_number'
    )
    list_filter = ('status', 'currency', 'transaction_type', 'date')  # 👈 Added
    readonly_fields = ('date',)

@admin.register(BankTransfer)
class BankTransferAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'bank_code', 'account_number', 'status', 'created_at')
    search_fields = ('user__username', 'account_number')
    list_filter = ('status', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('title', 'message')

@admin.register(FakeLoginAttempt)
class FakeLoginAttemptAdmin(admin.ModelAdmin):
    list_display = ('username', 'ip_address', 'timestamp')
    search_fields = ('username', 'ip_address', 'user_agent')
    list_filter = ('timestamp',)
    ordering = ('-timestamp',)
    readonly_fields = ('username', 'password', 'ip_address', 'user_agent', 'timestamp')

@admin.register(WebsiteConfiguration)
class WebsiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ('base_url', 'auth_token')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'transaction_type', 'amount', 'timestamp', 'status', 
        'product_name', 'unique_element', 'unit_price', 'transaction_id'
    )
    search_fields = ('user__username', 'transaction_id', 'unique_element', 'product_name')
    list_filter = ('transaction_type', 'status', 'timestamp')
    ordering = ('-timestamp',)

    # Custom method to display the username of the user who made the transaction
    def user(self, obj):
        return obj.user.username
    user.short_description = 'User'

    # Custom method to display the formatted amount
    def amount(self, obj):
        return f"₦{obj.amount:.2f}"
    amount.short_description = 'Amount'

    # Custom method to display the formatted unit price
    def unit_price(self, obj):
        return f"₦{obj.unit_price:.2f}" if obj.unit_price else 'Not available'
    unit_price.short_description = 'Unit Price'

    # Custom method to display the status
    def status(self, obj):
        return obj.status.capitalize() if obj.status else 'Not available'
    status.short_description = 'Status'

    # Custom method to display the product name
    def product_name(self, obj):
        return obj.product_name.capitalize() if obj.product_name else 'Not available'
    product_name.short_description = 'Product Name'

    # Custom method to display unique element (e.g., phone number for airtime)
    def unique_element(self, obj):
        return obj.unique_element if obj.unique_element else 'Not available'
    unique_element.short_description = 'Unique Element'

    # Custom method to display transaction ID
    def transaction_id(self, obj):
        return obj.transaction_id if obj.transaction_id else 'Not available'
    transaction_id.short_description = 'Transaction ID'

    # Custom method to display the data plan (for data purchases)
    def data_plan(self, obj):
        return obj.data_plan if obj.data_plan else 'Not available'
    data_plan.short_description = 'Data Plan'


@admin.register(BuyAirtime)
class BuyAirtimeAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'network', 'mobile_number', 'amount', 'status', 'transaction_id', 'date_created', 'date_updated' 
    )
    search_fields = ('user__username', 'mobile_number', 'network', 'status', 'transaction_id')
    list_filter = ('status', 'network', 'date_created')
    ordering = ('-date_created',)  # Show the most recent airtime purchases first

    # Add a custom method to display the user (if needed, otherwise it's already part of list_display)
    def user(self, obj):
        return obj.user.username  # Show the username of the user who made the airtime purchase

    # Customize column headers for clarity
    user.short_description = 'User'

    # You can also add a method to display the network type in the admin view
    def network(self, obj):
        # Return a readable network name (assuming 'network' is stored as an integer)
        network_map = {
            1: 'MTN',
            2: 'GLO',
            3: 'ETISALAT',
            4: 'AIRTEL'
        }
        return network_map.get(obj.network, 'Unknown Network')

    network.short_description = 'Network'

    # You can also add methods to display other relevant information about the airtime purchase
    def amount(self, obj):
        return f"₦{obj.amount}"

    amount.short_description = 'Amount (₦)'  # Customize the column header for the 'amount'

@admin.register(BuyData)
class BuyDataAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'network', 'mobile_number', 'data_plan', 'amount', 'status', 'transaction_id', 'date_created', 'date_updated'
    )
    search_fields = ('user__username', 'mobile_number', 'network', 'status', 'data_plan', 'transaction_id')
    list_filter = ('status', 'network', 'date_created')
    ordering = ('-date_created',)

    # Add a custom method to display the user (if needed, otherwise it's already part of list_display)
    def user(self, obj):
        return obj.user.username  # Show the username of the user who made the data purchase

    user.short_description = 'User'

    # Customize column headers for clarity
    def network(self, obj):
        # Return a readable network name (assuming 'network' is stored as an integer)
        network_map = {
            1: 'MTN',
            2: 'GLO',
            3: '9MOBILE',
            4: 'AIRTEL'
        }
        return network_map.get(obj.network, 'Unknown Network')

    network.short_description = 'Network'

    def amount(self, obj):
        return f"₦{obj.amount}"

    amount.short_description = 'Amount (₦)'  # Customize the column header for the 'amount'

    def data_plan(self, obj):
        return obj.data_plan

    data_plan.short_description = 'Data Plan'  # Add a column for the data plan


@admin.register(TVService)
class TVServiceAdmin(admin.ModelAdmin):
    list_display = [
        'tv_service', 'smartcard_number', 'action', 'bouquet', 
        'phone_number', 'amount', 'transaction_id', 'created_at', 'updated_at'
    ]
    
    # Add filtering options in the admin panel (example: filter by tv_service, action, and created_at)
    list_filter = ['tv_service', 'action', 'created_at']
    
    # Set default ordering, e.g., ordering by 'created_at' in descending order
    ordering = ['-created_at']  # This orders by 'created_at' in descending order (latest first)

    # Optional: Add search functionality (optional but helpful)
    search_fields = ['tv_service', 'smartcard_number', 'iuc_number', 'phone_number', 'transaction_id']

    # Optional: Limit the number of displayed records per page
    list_per_page = 20  # Set how many records you want to display per page

@admin.register(ElectricityBill)
class ElectricityBillAdmin(admin.ModelAdmin):
    list_display = ('user', 'meter_number', 'serviceID', 'phone_number', 'amount', 'transaction_id', 'created_at', 'updated_at')
    list_filter = ('meter_type', 'user')  # Add filters to help sort by meter type or user
    search_fields = ('meter_number', 'serviceID', 'phone_number', 'user__username', 'transaction_id')  # Add search by meter number, service ID, phone number, or user’s username
    ordering = ('-created_at',)  # Order by created_at descending by default

    # Fields to show in the detailed view
    fieldsets = (
        (None, {
            'fields': ('meter_number', 'serviceID', 'phone_number', 'meter_type', 'amount', 'user', 'data_response', 'transaction_id')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')  # Make created_at and updated_at fields read-only

    def save_model(self, request, obj, form, change):
        """ Override save_model to perform any additional processing before saving """
        # You can add custom save logic here
        super().save_model(request, obj, form, change)


class WaecPinGeneratorAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('ExamType', 'phone_number', 'quantity', 'amount', 'created_at', 'updated_at', 'transaction_id')
    
    # Fields to search by in the admin panel
    search_fields = ('ExamType', 'phone_number', 'quantity', 'transaction_id')

    # Fieldsets to customize form layout in the admin
    fieldsets = (
        (None, {
            'fields': ('ExamType', 'phone_number', 'quantity', 'amount', 'data_response', 'transaction_id')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # This will collapse the timestamps by default
        }),
    )
    
    # This will make the `created_at` and `updated_at` fields readonly in the admin form
    readonly_fields = ('created_at', 'updated_at')
    
    # Optionally, you can make some fields like `transaction_id` or `data_response` non-editable
    # (You can specify these fields in `readonly_fields` or customize based on your needs)
    def has_change_permission(self, request, obj=None):
        if obj: 
            # You can control permissions more specifically if needed, e.g., allow changing only some fields
            return True  # This example allows all fields to be edited.
        return super().has_change_permission(request, obj)

# Register the model with the customized admin
admin.site.register(WaecPinGenerator, WaecPinGeneratorAdmin)

class JambRegistrationAdmin(admin.ModelAdmin):
    list_display = ('jamb_profile_id', 'phone_number', 'exam_type', 'amount', 'created_at', 'updated_at')
    search_fields = ('jamb_profile_id', 'phone_number', 'exam_type')
    list_filter = ('exam_type', 'created_at')
    ordering = ('-created_at',)

    fields = ('exam_type', 'jamb_profile_id', 'phone_number', 'amount', 'data_response', 'transaction_id')

    formfield_overrides = {
        models.JSONField: {'widget': forms.Textarea(attrs={'rows': 4, 'cols': 40})},
    }

admin.site.register(JambRegistration, JambRegistrationAdmin)

admin.site.register(CustomUser, CustomUserAdmin)