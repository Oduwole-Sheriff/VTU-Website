from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    # Display the user, phone_number, address, full_name, and dob in the list view
    list_display = ('user', 'full_name', 'dob', 'phone_number', 'address')  
    
    # Allow searching by user, phone_number, address, full_name, and dob
    search_fields = ('user__username', 'full_name', 'phone_number', 'address')  
    
    # Allow filtering by user, and optionally by full_name and dob
    list_filter = ('user', 'full_name', 'dob')  

# Register the Profile model with the custom ProfileAdmin class
admin.site.register(Profile, ProfileAdmin)
