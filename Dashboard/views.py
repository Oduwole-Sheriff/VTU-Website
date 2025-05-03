from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import CustomUser, Transaction, Notification, MonnifyTransaction
from .forms import BuyAirtimeForm, BankTransferForm, BuyDataForm, TVServiceForm, ElectricityBillForm, WaecPinGeneratorForm, JambRegistrationForm
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db import transaction as db_transaction
from django.db.models import Sum, Q
from django.core.exceptions import ValidationError
from .forms import ReferralBonusTransferForm, NotificationForm
from django.contrib import messages
import json
from django.utils.timezone import now
import hmac
import hashlib
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal

from .forms import NINForm, CustomUserForm


# Create your views here.

def is_admin(user):
    return user.is_staff

def access_denied(request):
    return render(request, 'access_denied.html')

def Home(request):
    return render(request, 'home.html')

@csrf_exempt
def verify_monnify_signature(request, secret_key):
    signature = request.headers.get('monnify-signature')
    body = request.body
    expected_signature = hmac.new(
        key=secret_key.encode('utf-8'),
        msg=body,
        digestmod=hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(signature, expected_signature)

@csrf_exempt
def monnify_webhook(request):
    if request.method != "POST":
        return JsonResponse({"message": "Invalid request method"}, status=405)

    secret_key = 'WEDYDDCGYEX98Z7L31R1RZ4V6LK12JK9'

    if not verify_monnify_signature(request, secret_key):
        return JsonResponse({"message": "Invalid signature"}, status=400)

    try:
        payload = json.loads(request.body)
        print("📨 Full Webhook Payload:")
        print(json.dumps(payload, indent=4))

        event_type = payload.get("eventType")
        if event_type != "SUCCESSFUL_TRANSACTION":
            print("ℹ️ Ignored event:", event_type)
            return JsonResponse({"message": "Not a successful transaction"}, status=200)

        event_data = payload.get("eventData", {})
        payment_reference = event_data.get("paymentReference")
        amount_paid = float(event_data.get("amountPaid", 0))
        customer_email = event_data.get("customer", {}).get("email")
        account_reference = event_data.get("product", {}).get("reference")

        print(f"🔍 Reference: {payment_reference}")
        print(f"👤 Email: {customer_email}, AccountRef: {account_reference}")
        print(f"💵 Amount Paid: ₦{amount_paid:,.2f}")

        # Look up user by email, fallback to account reference
        try:
            user = CustomUser.objects.get(email=customer_email)
        except CustomUser.DoesNotExist:
            try:
                username_part = account_reference.split('_')[-1]
                user = CustomUser.objects.get(username=username_part)
            except CustomUser.DoesNotExist:
                print("❌ User not found")
                return JsonResponse({"message": "User not found"}, status=400)

        # Prevent double crediting
        if MonnifyTransaction.objects.filter(payment_reference=payment_reference).exists():
            print("⚠️ Duplicate transaction, skipping credit.")
            return JsonResponse({"message": "Duplicate webhook"}, status=200)

        # Credit user's wallet
        user.balance += Decimal(str(amount_paid))
        user.save()
        print(f"✅ Credited ₦{amount_paid:,.2f} to {user.username} (new balance: ₦{user.balance:,.2f})")

        # Handle first deposit reward (also deducts ₦50 and processes referral bonuses)
        from .utils import handle_first_deposit_reward
        handle_first_deposit_reward(user)

        # For subsequent deposits, deduct ₦35 Monnify fee
        if user.first_deposit_reward_given:
            if user.balance >= Decimal('35.00'):
                user.balance -= Decimal('35.00')
                user.save()
                print(f"💸 Deducted ₦35 Monnify fee for subsequent deposit. New balance: ₦{user.balance:,.2f}")
            else:
                print(f"⚠️ Not enough balance to deduct ₦35 fee after subsequent deposit.")

        # Save transaction
        MonnifyTransaction.objects.create(
            user=user,
            amount=amount_paid,
            payment_reference=payment_reference,
            monnify_transaction_reference=event_data.get("transactionReference"),
            bank_code=event_data.get("paymentSourceInformation", {}).get("bankCode", ""),
            account_number=event_data.get("paymentSourceInformation", {}).get("accountNumber", ""),
            narration=event_data.get("narration", "User Deposit"),
            status='successful',
            currency=event_data.get("currency", "NGN"),
            response_message=payload,
            transaction_type='first_deposit' if not user.first_deposit_reward_given else 'regular',
            date=now()
        )

        # Send confirmation email
        send_mail(
            subject="Wallet Credited",
            message=f"Hello {user.username},\n\nYour wallet has been credited with ₦{amount_paid:,.2f}.",
            from_email="no-reply@yourapp.com",
            recipient_list=[user.email],
            fail_silently=True,
        )

        return JsonResponse({"message": "Wallet credited successfully"}, status=200)

    except Exception as e:
        print("🔥 Error processing webhook:", e)
        return JsonResponse({"message": "Error processing webhook"}, status=400)

@login_required
def fund_wallet_form(request):
    user = request.user

    if request.method == 'POST':
        doc_type = request.POST.get('document_type')

        if doc_type == 'nin':
            form = NINForm(request.POST)
            if form.is_valid():
                user.nin = form.cleaned_data['nin']
                user.has_filled_fund_form = True
                user.save()
                return redirect('index')

        elif doc_type == 'bvn':
            form = CustomUserForm(request.POST, instance=user)
            if form.is_valid():
                user.bvn = form.cleaned_data['bvn']
                user.has_filled_fund_form = True
                user.save()
                return redirect('index')

    else:
        form = NINForm()

    return render(request, 'fund_wallet_form.html', {'form': form})


@login_required
@user_passes_test(is_admin, login_url='access-denied')
def Bank_Transfer(request):
    form = BankTransferForm()
    return render(request, 'bank_transfer.html', {'form': form})

@login_required
def transfer_referral_bonus_view(request):
    if not request.user.is_authenticated:
        return redirect('login')  # adjust to your login URL

    form = ReferralBonusTransferForm(request.POST or None, user=request.user)

    if request.method == 'POST' and form.is_valid():
        amount = form.cleaned_data['amount']
        try:
            request.user.transfer_referral_bonus_to_balance(amount)
            messages.success(request, f"Successfully transferred ₦{amount} to your balance.")
            return redirect('bonus-to-wallet')
        except Exception as e:
            messages.error(request, str(e))

    return render(request, 'bonus-to-wallet.html', {'form': form, 'user': request.user})

@login_required
@user_passes_test(is_admin, login_url='access-denied')
def create_notification(request):
    if request.method == "POST":
        form = NotificationForm(request.POST)
        if form.is_valid():
            notification = form.save(commit=False)

            if form.cleaned_data['send_to_all']:
                # Send to all users
                from django.contrib.auth import get_user_model
                User = get_user_model()
                users = User.objects.all()
                for user in users:
                    Notification.objects.create(
                        title=notification.title,
                        message=notification.message,
                        user=user
                    )
                messages.success(request, "Notification sent to all users.")
            else:
                notification.save()
                messages.success(request, "Notification sent to the selected user.")
            return redirect('create_notification')
    else:
        form = NotificationForm()
    
    return render(request, 'notifications.html', {'form': form})

@login_required
def Index(request):
    """Render the wallet balance page with total user balance and total registered users."""

    # Total metrics
    total_balance = CustomUser.objects.aggregate(total_balance=Sum('balance'))['total_balance'] or 0.00
    total_bonus = CustomUser.objects.aggregate(total_bonus=Sum('bonus'))['total_bonus'] or 0.00
    total_users = CustomUser.objects.count()

    # User-specific info
    balance = getattr(request.user, 'balance', 0.00)
    referral_bonus = request.user.referral_bonus or 0.00
    referral_link = request.build_absolute_uri(f"/register/?referral={request.user.username}")
    total_referrals = CustomUser.objects.filter(referred_by=request.user).count()

    # Transactions
    transactions = Transaction.objects.filter(user=request.user).order_by('-timestamp')
    paginator = Paginator(transactions, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Notifications (user-specific and default for all)
    notifications = Notification.objects.filter(
        Q(user=request.user) | Q(user__isnull=True)
    ).order_by('-created_at')

    return render(request, 'index.html', {
        'balance': balance,
        'total_balance': total_balance,
        'total_users': total_users,
        'total_bonus': total_bonus,
        'transactions': transactions,
        'page_obj': page_obj,
        'referral_link': referral_link,
        'total_referrals': total_referrals,
        'referral_bonus': referral_bonus,
        'notifications': notifications,
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
    return render(request, 'tv-subscription.html', {'form': form, 'user_balance': user.balance})

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
    return render(request, 'waec.html', {'form': form, 'user_balance': user.balance})

@login_required
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
def EducationReceiptJamb(request):
    return render(request, 'Educaional-receipt-jamb.html')

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
