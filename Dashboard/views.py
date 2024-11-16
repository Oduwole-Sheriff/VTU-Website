from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Transaction
# from django.contrib import messages

# Create your views here.

def Home(request):
    return render(request, 'home.html')

@login_required
def Index(request):
    """Render the wallet balance page."""
    # Ensure the 'balance' is coming from CustomUser model, assuming one-to-one relation with User
    try:
        # CustomUser has a OneToOne relation with User, so access CustomUser through user
        balance = request.user.balance  # Or use `request.user.balance` if it's directly on the User model
    except CustomUser.DoesNotExist:
        balance = 0  # Default to 0 if the CustomUser instance doesn't exist
    
    # Render the template with the wallet balance
    return render(request, 'index.html', {'balance': balance})


@login_required
def transaction_history(request):
    """Render the transaction history for the logged-in user."""
    transactions = Transaction.objects.filter(user=request.user).order_by('-timestamp')  # Correcting field name to 'timestamp'

    return render(request, 'transaction_history.html', {'transactions': transactions})

@login_required
def BuyData(request):
    return render(request, 'buy-data.html')

@login_required
def BuyAirtime(request):
    return render(request, 'buy-airtime.html')

@login_required
def ManageSubscription(request):
    return render(request, 'manage-subscription.html')

@login_required
def BillPayment(request):
    return render(request, 'bill-payment.html')

@login_required
def CableSubscription(request):
    return render(request, 'cable-subscription.html')

@login_required
def BuyDataCard(request):
    return render(request, 'buy-dataCard.html')

@login_required
def BuyDataPin(request):
    return render(request, 'buy-dataPin.html')

@login_required
def AirtimeToCash(request):
    return render(request, 'airtime-to-cash.html')

@login_required
def BonusToWallet(request):
    return render(request, 'bonus-to-wallet.html')

@login_required
def BulkSMS(request):
    return render(request, 'bulk-sms.html')

@login_required
def ResultChecker(request):
    return render(request, 'result-checker.html')
