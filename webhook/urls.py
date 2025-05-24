from django.urls import path
from .views import WebhookView, process_webhook


urlpatterns = [
    path('api/v1/webhook_listen/', process_webhook, name='process_webhook'),
    path("api/v1/webhook_listener", WebhookView.as_view(), name="webhook_processor"),
    # path('api/webhooks/monnify/', WebhookView.as_view(), name='monnify-webhook'),
]
