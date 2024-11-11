from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='home-page'),
    path('index/', views.Index, name='index'),
    path('data/', views.BuyData, name='buydata'),
    path('airtimeTopUp/', views.BuyAirtime, name='buy_airtime'),
    path('billPayment/', views.BillPayment, name='bill_payment'),
    path('cableSubscription/', views.CableSubscription, name='cable_subscription'),
    path('manageSubscription/', views.ManageSubscription, name='manage_subscription'),
]