from django.apps import AppConfig
from django.db import IntegrityError
from django.conf import settings
from django.db.models.signals import post_migrate
from django.dispatch import receiver

class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Dashboard'

    def ready(self):
        """
        This method is triggered when the app is loaded. We will import the model 
        and connect the signal here to ensure the app registry is fully loaded.
        """
        import Dashboard.signals
        from Dashboard.models import WebsiteConfiguration  # Import inside ready() to ensure app is ready
        
        def populate_monnify_configuration(sender, **kwargs):
            try:
                # Check if WebsiteConfiguration already exists
                config = WebsiteConfiguration.objects.first()

                if not config:  # If there's no configuration, insert default values
                    WebsiteConfiguration.objects.create(
                        base_url=settings.MONNIFY_BASE_URL,
                        auth_token=settings.MONNIFY_AUTH_TOKEN
                    )
                    print("Monnify API Configuration has been added to the database.")
                else:
                    print("Monnify API Configuration already exists in the database.")
            except IntegrityError:
                # Handle any potential errors related to database constraints
                print("Error while trying to populate Monnify configuration.")

        # Connect the signal to populate Monnify configuration after migrations
        post_migrate.connect(populate_monnify_configuration, sender=self)
