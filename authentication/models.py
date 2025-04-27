from django.db import models
from django.conf import settings
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=11, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)  # Added full_name field
    dob = models.DateField(blank=True, null=True)  # Added dob field
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
