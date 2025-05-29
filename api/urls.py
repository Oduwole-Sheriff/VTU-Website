from django.urls import path
from api.views import RegisterAPI, LoginAPI, BankTransferAPIView, PaystackWebhookView, PublicIPView, InitializeTransactionView, PaystackConfigView, PaystackTransactionListView, WebhookView, TransferBonusAPIView, WithdrawView, TransferView, TransactionListView, SubmitAccountDetailsView, BuyAirtimeView, BuyDataAPIView, TVServiceAPIView, ElectricityBillCreateView, WaecPinGeneratorCreateView, JambRegistrationViewSet

urlpatterns = [
    path('registration/', RegisterAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('monnify/webhook/', WebhookView.as_view(), name='monnify-webhook'),
    path('bank-transfer/', BankTransferAPIView.as_view(), name='bank_transfer_api'),
    path('paystack/config/', PaystackConfigView.as_view(), name='paystack-config'),
    path("debug/ip/", PublicIPView.as_view(), name="public-ip"),
    path('paystack/initialize/', InitializeTransactionView.as_view(), name='paystack-initialize'),
    path('paystack/transactions/', PaystackTransactionListView.as_view(), name='paystack-transactions'),
    path('paystack/webhook/', PaystackWebhookView.as_view(), name='paystack-webhook'),
    path("bonus-to-bank/", TransferBonusAPIView.as_view(), name="bonus-transfer"),
    path('withdraw/', WithdrawView.as_view(), name='withdraw'),
    path('transfer/', TransferView.as_view(), name='transfer'),
    path('transactions/', TransactionListView.as_view(), name='transaction_list'),
    path('submit-account-details/', SubmitAccountDetailsView.as_view(), name='submit_account_details'),
    path('buy-airtime/', BuyAirtimeView.as_view(), name='buy_airtime'),
    path('buy-data/', BuyDataAPIView.as_view(), name='buy-data'),
    path('tvservice/', TVServiceAPIView.as_view(), name='tvservice'),
    path('electricity-bill/', ElectricityBillCreateView.as_view(), name='electricity-bill'),
    path('waec-registration/', WaecPinGeneratorCreateView.as_view(), name='waec-registration'),
    path('jamb-registration/', JambRegistrationViewSet.as_view(), name='jamb-registration'),
]  