from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Transaction
from .forms import BuyAirtimeForm, BuyDataForm, TVServiceForm, ElectricityBillForm, WaecPinGeneratorForm, JambRegistrationForm
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db import transaction as db_transaction
from django.db.models import Sum
from django.core.exceptions import ValidationError
# from django.contrib import messages

# Create your views here.

def Home(request):
    return render(request, 'home.html')

@login_required
def Index(request):
    """Render the wallet balance page with total user balance and total registered users."""

    # Total user balance: Sum of all user balances
    total_balance = CustomUser.objects.aggregate(total_balance=Sum('balance'))['total_balance'] or 0.00

    # Total user bonus: Sum of all user bonus
    total_bonus = CustomUser.objects.aggregate(total_bonus=Sum('bonus'))['total_bonus'] or 0.00
    
    # Total registered users: Count of all users
    total_users = CustomUser.objects.count()

    # Get the balance of the logged-in user
    try:
        balance = request.user.balance  # Assuming balance is on CustomUser and it's linked to the logged-in user
    except CustomUser.DoesNotExist:
        balance = 0  # Default to 0 if the CustomUser instance doesn't exist

    # Render the template and pass the data to the template context
    return render(request, 'index.html', {
        'balance': balance,
        'total_balance': total_balance,
        'total_users': total_users,
        'total_bonus': total_bonus,
    })


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
def ElectricityBillPayment(request):
    user = request.user  # Get the logged-in user

    if request.method == 'POST':
        form = ElectricityBillForm(request.POST)

        if form.is_valid():
            electricity_bill = form.save(commit=False)  # Don’t save yet to perform additional actions

            amount = form.cleaned_data['amount']

            # Check if the user's balance is sufficient to pay for the electricity bill
            if user.balance < amount:
                return JsonResponse({'status': 'error', 'message': "Insufficient balance to complete the payment."})

            # Save the electricity bill purchase record
            electricity_bill.save()

            # Deduct the amount from the user's balance
            user.balance -= amount
            user.save()  # Save the updated balance

            # Log the transaction for the electricity bill payment
            Transaction.objects.create(
                user=user,
                transaction_type='electricity_payment',
                amount=amount,
                recipient=None,  # No recipient for electricity payment
                description=f"Payment for electricity bill with meter number {electricity_bill.meter_number}"
            )

            # Return a success response
            return JsonResponse({'status': 'success', 'message': 'Payment successful!'})

    else:
        form = ElectricityBillForm()

    # Render the form in the template
    return render(request, 'bill-payment.html', {'form': form, 'user_balance': user.balance})

@login_required
def TVSubscription(request):
    user = request.user  # Get the logged-in user

    if request.method == 'POST':
        form = TVServiceForm(request.POST)
        
        # Validate the form first
        if form.is_valid():
            tv_service_instance = form.save(commit=False)  # Don't save to DB yet

            # Get the subscription amount from the form
            amount = form.cleaned_data['amount']

            # Check if the user's balance is sufficient to pay for the TV service
            if user.balance < amount:
                return JsonResponse({'status': 'error', 'message': "Insufficient balance to complete the subscription."}, status=400)

            try:
                # Call the process_purchase method to check if balance is sufficient and deduct the amount
                tv_service_instance.process_purchase()

                # After successful processing, save the subscription to the database
                tv_service_instance.save()

                # Deduct the amount from the user's balance
                user.balance -= amount
                user.save()  # Save the updated balance

                # Log the transaction for the TV service subscription
                Transaction.objects.create(
                    user=user,
                    transaction_type='tv_subscription',
                    amount=amount,
                    recipient=None,  # No recipient for TV subscription
                    description=f"Subscription to TV service {tv_service_instance.service_name} (ID: {tv_service_instance.id})"
                )

                # Return a success response
                return JsonResponse({'status': 'success', 'message': 'Subscription successful!'})

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

    # Render the form in the template
    return render(request, 'tv-subscription.html', {'form': form})

@login_required
def Waec(request):
    user = request.user  # Get the logged-in user

    if request.method == 'POST':
        form = WaecPinGeneratorForm(request.POST)

        # Validate the form first
        if form.is_valid():
            waec_pin_instance = form.save(commit=False)  # Don't save to DB yet

            # Get the amount and quantity from the form
            amount = form.cleaned_data['amount']
            quantity = form.cleaned_data['quantity']

            # Example logic to check if the user has enough balance (adjust according to your model's logic)
            if user.balance < amount * quantity:
                return JsonResponse({'status': 'error', 'message': "Insufficient balance to generate the pins."}, status=400)

            try:
                # Call any relevant method to process the pin generation logic
                # For example, generate pins or process the purchase, if necessary
                waec_pin_instance.process_purchase()

                # After successful processing, save the pin instance to the database
                waec_pin_instance.save()

                # Deduct the total amount from the user's balance
                user.balance -= amount * quantity
                user.save()  # Save the updated balance

                # Log the transaction for the WAEC result pin generation
                Transaction.objects.create(
                    user=user,
                    transaction_type='waec_pin_generation',
                    amount=amount * quantity,
                    recipient=None,  # No recipient for pin generation
                    description=f"Generated {quantity} WAEC pins (ID: {waec_pin_instance.id})"
                )

                # Return a success response
                return JsonResponse({'status': 'success', 'message': f'{quantity} WAEC pins generated successfully!'})

            except ValidationError as e:
                # Return an error response in case of issues during processing
                error_data = {
                    'status': 'error',
                    'message': str(e),
                }
                return JsonResponse(error_data, status=400)
        else:
            # Return an error response if the form is not valid
            return JsonResponse({'status': 'error', 'message': 'Form is invalid'}, status=400)
    else:
        form = WaecPinGeneratorForm()

    # Render the form in the template
    return render(request, 'waec.html', {'form': form})

def JambRegistrationPayment(request):
    user = request.user  # Get the logged-in user

    if request.method == 'POST':
        form = JambRegistrationForm(request.POST)

        if form.is_valid():
            jamb_registration = form.save(commit=False)  # Don’t save yet to perform additional actions

            # Get the amount (if any logic is associated with the amount)
            amount = form.cleaned_data['amount']

            # Check if the user's balance is sufficient for registration
            if user.balance < amount:
                return JsonResponse({'status': 'error', 'message': "Insufficient balance to complete the registration."})

            # Save the JAMB registration record
            jamb_registration.save()

            # Deduct the amount from the user's balance
            user.balance -= amount
            user.save()  # Save the updated balance

            # Log the transaction for the JAMB registration payment
            Transaction.objects.create(
                user=user,
                transaction_type='jamb_registration',
                amount=amount,
                recipient=None,  # No recipient for JAMB registration
                description=f"Payment for JAMB registration with Profile ID {jamb_registration.jamb_profile_id}"
            )

            # Return a success response
            return JsonResponse({'status': 'success', 'message': 'JAMB registration successful!'})

    else:
        form = JambRegistrationForm()

    # Render the form in the template, passing the user's balance
    return render(request, 'jamb.html', {'form': form, 'user_balance': user.balance})

@login_required
def EducationReceipt(request):
    return render(request, 'Educaional-receipt.html')

@login_required
def receipt(request):
    return render(request, 'receipt.html')


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
