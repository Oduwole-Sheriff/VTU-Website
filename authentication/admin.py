from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address')  # Display user, phone_number, and address
    search_fields = ('user__username', 'phone_number', 'address')  # Allow searching by user, phone_number, or address
    list_filter = ('user',)  # Optionally, allow filtering by user

# Register the Profile model with the custom ProfileAdmin class
admin.site.register(Profile, ProfileAdmin)
