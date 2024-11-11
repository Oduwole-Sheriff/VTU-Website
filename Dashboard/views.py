from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# from django.contrib import messages

# Create your views here.

def Home(request):
    return render(request, 'home.html')

@login_required
def Index(request):
    return render(request, 'index.html')

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
