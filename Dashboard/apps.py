from django.apps import AppConfig
from django.db import IntegrityError

class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Dashboard'

    def ready(self):
        import Dashboard.signals
        from django.db.models.signals import post_migrate
        from django.dispatch import receiver
        from django.conf import settings
        from Dashboard.models import WebsiteConfiguration

        @receiver(post_migrate)
        def populate_monnify_configuration(sender, **kwargs):
            try:
                config = WebsiteConfiguration.objects.first()
                if not config:
                    base_url = getattr(settings, "MONNIFY_BASE_URL", None)
                    auth_token = getattr(settings, "MONNIFY_AUTH_TOKEN", None)

                    if base_url and auth_token:
                        WebsiteConfiguration.objects.create(
                            base_url=base_url,
                            auth_token=auth_token
                        )
                        print("Monnify API Configuration has been added to the database.")
                    else:
                        print("Monnify base URL or auth token not set in settings.")
                else:
                    print("Monnify API Configuration already exists in the database.")
            except IntegrityError:
                print("Error while trying to populate Monnify configuration.")

        post_migrate.connect(populate_monnify_configuration)

