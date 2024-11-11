from django.urls import path
from api.views import RegisterAPI, LoginAPI

urlpatterns = [
    path('registration/', RegisterAPI.as_view()),
    path('login/', LoginAPI.as_view()),
]