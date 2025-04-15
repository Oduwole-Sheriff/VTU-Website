from django.urls import path
from api.views import RegisterAPI, LoginAPI, DepositAPIView, WithdrawView, TransferView, TransactionListView, SubmitAccountDetailsView, BuyAirtimeView, BuyDataAPIView, TVServiceAPIView, ElectricityBillCreateView, WaecPinGeneratorCreateView, JambRegistrationViewSet

urlpatterns = [
    path('registration/', RegisterAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('deposit/', DepositAPIView.as_view(), name='deposit-api'),
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