from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='home-page'),
    path('deposit/', views.deposit_view, name='deposit'),
    path('Bonus-to-wallet/', views.transfer_referral_bonus_view, name='bonus-to-wallet'),
    path('Bank_Transfer/', views.Bank_Transfer, name='Bank_Transfer'),
    path('Create-Notification/', views.create_notification, name='create_notification'),
    path('index/', views.Index, name='index'),
    path('transactions/', views.transaction_history, name='transaction_history'), 
    path('data/', views.BuyData, name='buydata'),
    path('airtimeTopUp/', views.BuyAirtime, name='airtime-topUp'),
    path('billpayment/', views.ElectricityBillPayment, name='bill_payment'),
    path('cableSubscription/', views.TVSubscription, name='cable_subscription'),
    path('receipt/', views.receipt, name='receipt'),
    path('manageSubscription/', views.ManageSubscription, name='manage_subscription'),
    path('waec-registration/', views.Waec, name='waec'),
    path('jamb-registration/', views.JambRegistrationPayment, name='jamb'),
    path('Edu-Receipt/', views.EducationReceipt, name='Edu-Receipt'),
    path('Edu-Jamb-Receipt/', views.EducationReceiptJamb, name='Edu-Jamb-Receipt'),

    path('dataCard/', views.BuyDataCard, name='buy_dataCard'),
    path('dataRecharge-Pin-Order/', views.BuyDataPin, name='buy_dataPin'),
    path('Airtime-Funding/', views.AirtimeToCash, name='airtime_to_Cash'),
    path('Bulk-SMS/', views.BulkSMS, name='bulk-sms'),
    path('Result-Checker/', views.ResultChecker, name='result-checker'),
]