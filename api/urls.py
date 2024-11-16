from django.urls import path
from api.views import RegisterAPI, LoginAPI, DepositView, WithdrawView, TransferView, TransactionListView

urlpatterns = [
    path('registration/', RegisterAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('deposit/', DepositView.as_view(), name='deposit'),
    path('withdraw/', WithdrawView.as_view(), name='withdraw'),
    path('transfer/', TransferView.as_view(), name='transfer'),
    path('transactions/', TransactionListView.as_view(), name='transaction_list'),
]   
    