from django.urls import path
from api.views import RegisterAPI, LoginAPI, WalletBalanceView, DepositView, WithdrawView, TransferView

urlpatterns = [
    path('registration/', RegisterAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('wallet/balance/', WalletBalanceView.as_view(), name='get_wallet_balance'),
    path('wallet/deposit/', DepositView.as_view(), name='deposit'),
    path('wallet/withdraw/', WithdrawView.as_view(), name='withdraw'),
    path('wallet/transfer/', TransferView.as_view(), name='transfer'),
]   
    