from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Transaction
from .forms import BuyAirtimeForm, BuyDataForm, TVServiceForm
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db import transaction as db_transaction
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

    # Paginate the transactions (10 transactions per page, you can change this number)
    paginator = Paginator(transactions, 10)
    
    # Get the current page number from the request
    page_number = request.GET.get('page')
    
    # Get the transactions for the current page
    page_obj = paginator.get_page(page_number)

    return render(request, 'transaction_history.html', {'transactions': transactions, 'page_obj': page_obj})


@login_required
def BuyData(request):
    user = request.user  # Get the logged-in user

    if request.method == 'POST':
        # Pass the logged-in user to the form
        form = BuyDataForm(request.POST)

        if form.is_valid():
            buy_data = form.save(commit=False)  # Do not commit yet, to perform additional actions
            amount = form.cleaned_data['amount']

            # Check if the user's balance is less than the amount
            if user.balance < amount:
                return JsonResponse({'status': 'error', 'message': "Insufficient balance to complete the purchase."})

            # Proceed with saving the BuyData record
            buy_data.user = user  # Set the user manually before saving
            buy_data.save()  # Save the data purchase record

            # Update user's balance
            user.balance -= amount
            user.save()  # Save the updated balance

            # Log the transaction for the data purchase
            with db_transaction.atomic():  # Ensure the balance update and transaction creation happen atomically
                Transaction.objects.create(
                    user=user,
                    transaction_type='data_purchase',
                    amount=amount,
                    recipient=None,  # No recipient in data purchase
                    description=f"Purchase of {buy_data.data_plan} data plan for {buy_data.mobile_number}"
                )

            # Return success response
            return JsonResponse({'status': 'success', 'message': 'Data purchase successful.'})

        else:
            # If the form is invalid, return the error message
            return JsonResponse({'status': 'error', 'message': 'Form is invalid.'})

    else:
        form = BuyDataForm()

    # Render the form in the 'buy-data.html' template
    return render(request, 'buy-data.html', {'form': form, 'user_balance': user.balance})


@login_required
def BuyAirtime(request):
    user = request.user  # Get the logged-in user

    if request.method == 'POST':
        # Pass the logged-in user to the form
        form = BuyAirtimeForm(request.POST, user=user)  # Set the user

        if form.is_valid():
            buy_airtime = form.save(commit=False)  # Do not commit yet, to perform additional actions

            amount = form.cleaned_data['amount']

            # Check if the user's balance is less than the amount
            if user.balance < amount:
                return JsonResponse({'status': 'error', 'message': "Insufficient balance to complete the purchase."})

            # Proceed with saving the BuyAirtime record
            buy_airtime.save()  # Save the airtime purchase record

            # Update user's balance
            user.balance -= amount
            user.save()  # Save the updated balance

            # Log the transaction for the airtime purchase
            Transaction.objects.create(
                user=user,
                transaction_type='airtime_purchase',
                amount=amount,
                recipient=None,  # No recipient in airtime purchase
                description=f"Purchase of {buy_airtime.data_type} airtime for {buy_airtime.mobile_number}"
            )

            # Return success response
            return JsonResponse({'status': 'success'})

    else:
        form = BuyAirtimeForm()

    # Render the form in the 'buy-airtime.html' template
    return render(request, 'buy-airtime.html', {'form': form, 'user_balance': user.balance})

@login_required
def ManageSubscription(request):
    return render(request, 'manage-subscription.html')

@login_required
def BillPayment(request):
    return render(request, 'bill-payment.html')

@login_required
def TVSubscription(request):
    if request.method == 'POST':
        form = TVServiceForm(request.POST)
        
        # Validate the form first
        if form.is_valid():
            tv_service_instance = form.save(commit=False)  # Don't save to DB yet
            try:
                # Call the process_purchase method to check if balance is sufficient and deduct the amount
                tv_service_instance.process_purchase()

                # After successful processing, return a success response (simulating a transaction)
                # Optionally, you can simulate a transaction log here
                Transaction.objects.create(
                    user=user,
                    transaction_type='airtime_purchase',
                    amount=amount,
                    recipient=None,  # No recipient in airtime purchase
                    description=f"Purchase of {buy_airtime.data_type} airtime for {buy_airtime.mobile_number}"
                )

                # Return the response as JSON
                return JsonResponse(Transaction, {'status': 'success'}, status=400)
            except ValidationError as e:
                # Return an error response in case of insufficient balance or invalid amount
                error_data = {
                    'status': 'error',
                    'message': str(e),
                }
                return JsonResponse(error_data, status=400)
        else:
            # Return an error response if the form is not valid
            return JsonResponse({'status': 'error', 'message': 'Form is invalid'}, status=400)
    else:
        form = TVServiceForm()
    
    return render(request, 'tv-subscription.html', {'form': form})


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
