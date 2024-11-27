from django.contrib.auth import views as auth_views
from django.urls import path
from . import views as user_views
urlpatterns = [
    path('register/', user_views.register, name='register'),
    path('update-profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', user_views.custom_logout, name='logout'),  
]