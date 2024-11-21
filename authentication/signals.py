from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Profile

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    """ Creates a profile for the user when a new user is created """
    if created:
        # Ensure that a profile is only created once
        Profile.objects.get_or_create(user=instance)
        
    # No need to save the profile here as it is already saved automatically
    # instance.profile.save()  # This line is unnecessary and can be removed

