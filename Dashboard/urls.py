from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='home-page'),
    path('index/', views.Index, name='index'),
    path('transactions/', views.transaction_history, name='transaction_history'), 
    path('data/', views.BuyData, name='buydata'),
    path('airtimeTopUp/', views.BuyAirtime, name='buy_airtime'),
    path('billPayment/', views.BillPayment, name='bill_payment'),
    path('cableSubscription/', views.CableSubscription, name='cable_subscription'),
    path('manageSubscription/', views.ManageSubscription, name='manage_subscription'),

    path('dataCard/', views.BuyDataCard, name='buy_dataCard'),
    path('dataRecharge-Pin-Order/', views.BuyDataPin, name='buy_dataPin'),
    path('Airtime-Funding/', views.AirtimeToCash, name='airtime_to_Cash'),
    path('Transfer-Bonus/', views.BonusToWallet, name='bonus-to-wallet'),
    path('Bulk-SMS/', views.BulkSMS, name='bulk-sms'),
    path('Result-Checker/', views.ResultChecker, name='result-checker'),
]