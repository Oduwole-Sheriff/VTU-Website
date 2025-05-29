# import time
# from django.shortcuts import render, redirect, get_object_or_404
# from django.http import JsonResponse
# from rest_framework.exceptions import ValidationError

# from authentication.models import Profile

from rest_framework.permissions import IsAuthenticated
# from rest_framework.authentication import TokenAuthentication

# from django.contrib.auth import authenticate
# from drf_yasg.utils import swagger_auto_schema

from decimal import Decimal

import requests

from django.http import HttpResponse, HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from decimal import InvalidOperation


import hmac
import hashlib
from django.core.mail import send_mail
from django.db.models import Sum
from django.conf import settings

from api.serializer import RegisterSerializer, LoginSerializer, CustomUserSerializer, BankTransferSerializer, PaystackTransactionSerializer, WithdrawSerializer, TransferSerializer, TransactionSerializer, AccountDetailsSerializer, BuyAirtimeSerializer, BuyDataSerializer, TVServiceSerializer, ElectricityBillSerializer, WaecPinGeneratorSerializer, JambRegistrationSerializer
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from django.contrib.auth import authenticate, login
from Dashboard.models import CustomUser, BankTransfer, MonnifyTransaction, PaystackTransaction, Transaction, TVService, ElectricityBill, WaecPinGenerator, JambRegistration
from django.db import IntegrityError
from django.http import JsonResponse
from rest_framework.exceptions import ValidationError

from django.db import transaction as db_transaction

from Dashboard.utils import handle_first_deposit_reward
from django.utils.timezone import now
import traceback
from rest_framework.decorators import api_view

from rest_framework.generics import ListAPIView

from RestAPI.AirtimeAPI import VTPassAPI
from RestAPI.DataAPI import VTPassDataAPI
from RestAPI.TVSubscriptionAPI import  VTPassTVSubscription   
from RestAPI.ElectricityAPI import  VTPassElectricity
from RestAPI.EducationalAPI import VTPassEducationAPI
from RestAPI.MonnifyPayout import MonnifyBankTransferAPI

import uuid
from datetime import datetime
# import logging
import json
import random
from datetime import datetime as Mdate  

import os

from django.contrib.auth import get_user_model
User = get_user_model()  # Get the custom user model


class RegisterAPI(APIView):

    def post(self, request):
        # Parse incoming request data
        data = request.data
        serializer = RegisterSerializer(data=data)
        
        # Validate the data
        if not serializer.is_valid():
            # Return validation errors if serializer is invalid
            return Response({
                'status': False,
                'message': 'Validation failed',
                'errors': serializer.errors  # Provide detailed validation errors
            }, status=status.HTTP_400_BAD_REQUEST)

        # Save the user after validation
        user = serializer.save()

        # Return success response with username of the newly created user
        return Response({
            'status': True,
            'message': 'User successfully created',
            'username': user.username  # Return the username of the created user
        }, status=status.HTTP_201_CREATED)



class LoginAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        
        # Validate the serializer
        if not serializer.is_valid():
            return Response({
                'status': False,
                'message': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        # Extract username and password from the validated data
        username = serializer.data['username']
        password = serializer.data['password']
        
        # Try to authenticate the user
        user = authenticate(request, username=username, password=password)
        
        # Check if the user exists
        if not user:
            # Check if the username exists in the database
            if not CustomUser.objects.filter(username=username).exists():
                return Response({
                    'status': False,
                    'message': "Username does not exist"
                }, status=status.HTTP_400_BAD_REQUEST)
            # If username exists but password is incorrect
            else:
                existing_user = CustomUser.objects.get(username=username)

                # Increment failed attempts
                existing_user.failed_attempts += 1

                # Lock account if needed
                if existing_user.failed_attempts >= 5:
                    existing_user.save()
                    return Response({
                        'status': False,
                        'message': "Your account has been locked after 5 failed login attempts. Please contact support."
                    }, status=status.HTTP_403_FORBIDDEN)

                # Save the user with updated failed attempts
                existing_user.save()

                # Optional warning message
                warning_message = "Invalid password"
                if existing_user.failed_attempts >= 3:
                    warning_message += ". Warning: Your account will be locked after 5 failed attempts."

                return Response({
                    'status': False,
                    'message': warning_message
                }, status=status.HTTP_400_BAD_REQUEST)

        # Reset failed_attempts on successful login
        user.failed_attempts = 0
        user.save()

        # If authentication is successful, get or create the token
        token, created = Token.objects.get_or_create(user=user)
        
        # Log the user in
        login(request, user)

        # Return a successful response with the token
        return Response({
            'status': True, 
            'message': 'User logged in',
            'token': token.key,
            'redirect_url': '/'
        }, status=status.HTTP_200_OK)
    
class SubmitAccountDetailsView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user  # Get the current logged-in user
        serializer = AccountDetailsSerializer(user, data=request.data)

        if serializer.is_valid():
            try:
                # Attempt to update the user
                serializer.save()

                # Fetch the account details after saving
                account_details = _get_account_details(user)

                # Store a session flag to indicate form submission was successful
                request.session['form_submitted'] = True
                
                # Return the updated account details in the response
                return Response({
                    "success": True,
                    "account_details": account_details
                }, status=status.HTTP_200_OK)

            except IntegrityError:
                return Response({
                    "success": False,
                    "error": "The BVN is already associated with another user."
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "success": False,
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    
def _get_account_details(user):
    """ Helper function to extract bank account details """
    account_details = []
    if user.bank_account and 'accounts' in user.bank_account:
        for account in user.bank_account['accounts']:
            account_info = {
                'bank_name': account.get('bankName', 'No Bank Name'),
                'account_name': account.get('accountName', 'No Account Name'),
                'account_number': account.get('accountNumber', 'No Account Number')
            }
            account_details.append(account_info)
    return account_details


class TransferBonusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        try:
            result = user.transfer_bonus_to_platform()
            return Response({"message": "Bonus transferred successfully", "details": result}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

class WithdrawView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = WithdrawSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            user = request.user  # Assuming the user is authenticated

            # Check if the amount is positive
            if amount <= 0:
                return Response({"detail": "Amount must be positive."}, status=status.HTTP_400_BAD_REQUEST)

            # Withdraw funds from the user's balance
            try:
                user.withdraw(amount)
            except ValueError as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            return Response(CustomUserSerializer(user).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransferView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = TransferSerializer(data=request.data)
        if serializer.is_valid():
            recipient_id = serializer.validated_data['recipient_id']
            amount = serializer.validated_data['amount']
            user = request.user  # Assuming the user is authenticated

            # Check if the amount is positive
            if amount <= 0:
                return Response({"detail": "Amount must be positive."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                recipient = CustomUser.objects.get(id=recipient_id)
            except CustomUser.DoesNotExist:
                return Response({"detail": "Recipient not found."}, status=status.HTTP_404_NOT_FOUND)

            # Transfer funds from the user to the recipient
            try:
                user.transfer(recipient, amount)
            except ValueError as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            # Return the updated user and recipient balance info
            return Response({
                "user_balance": CustomUserSerializer(user).data,
                "recipient_balance": CustomUserSerializer(recipient).data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# views.py (with filtering)
class TransactionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transaction_type = request.query_params.get('transaction_type', None)
        
        # Get transactions for the authenticated user
        transactions = Transaction.objects.filter(user=request.user)
        
        if transaction_type:
            transactions = transactions.filter(transaction_type=transaction_type)

        transactions = transactions.order_by('-timestamp')
        print(transactions)

        # Serialize the data
        serializer = TransactionSerializer(transactions, many=True)
        print(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)


your_secret_key = os.environ["MONNIFY_CLIENT_SECRET"]  # Your Monnify Secret key
monnify_ip = os.environ["MONNIFY_IP"]  # Monnify IP address which is: 35.242.133.146


def verify_hash(payload_in_bytes, monnify_hash):
    secret_key_bytes = os.environ["MONNIFY_CLIENT_SECRET"].encode("utf-8")
    your_hash_in_bytes = hmac.new(
        secret_key_bytes, msg=payload_in_bytes, digestmod=hashlib.sha512
    )
    your_hash_in_hex = your_hash_in_bytes.hexdigest()
    return hmac.compare_digest(your_hash_in_hex, monnify_hash)



def get_sender_ip(headers):
    """
    Get senders' IP address, by first checking if your API server
    is behind a proxy by checking for HTTP_X_FORWARDED_FOR
    if not gets sender actual IP address using REMOTE_ADDR
    """

    x_forwarded_for = headers.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        # in some cases this might be in the second index ie [1]
        # depending on your hosting environment
        return x_forwarded_for.split(",")[0]
    else:
        return headers.get("REMOTE_ADDR")


def verify_monnify_webhook(payload_in_bytes, monnify_hash, headers):
    """
    The interface that does the verification by calling necessary functions.
    Though everything has been tested to work well, but if you have issues
    with this function returning False, you can remove the get_sender_ip
    function to be sure that the verify_hash is working, then you can check
    what header contains the IP address.
    """

    return get_sender_ip(headers) == monnify_ip and verify_hash(
        payload_in_bytes, monnify_hash
    )

@api_view(["POST"])
def process_webhook(request):
    """
    A function based view implementing the receipt of the webhook payload.
    The webhook payload should be received as bytes rather than json
    that would be converted to bytes.This is most likely one of the
    cause for failed webhook verification.
    After the webhook verification, you can get a json format of the byte
    object by simply calling json.loads(payload_in_bytes)
    """

    payload_in_bytes = request.body
    monnify_hash = request.META["HTTP_MONNIFY_SIGNATURE"]
    confirmation = verify_monnify_webhook(payload_in_bytes, monnify_hash, request.META)
    if confirmation is False:
        return Response(
            {"status": "failed", "msg": "Webhook does not appear to come from Monnify"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    else:
        """
        if payload verification is successful, you can perform your necessary task,
        but if your planned processing would take time, you should first return a 200 response
        and process your stuff in background.
        """
        return Response(
            {"status": "success", "msg": "Webhook received successfully"},
            status=status.HTTP_200_OK,
        )

class WebhookView(APIView):
    def post(self, request):
        payload_in_bytes = request.body
        monnify_hash = request.META.get("HTTP_MONNIFY_SIGNATURE")

        if not monnify_hash:
            return Response(
                {"status": "failed", "message": "Missing Monnify signature"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not verify_monnify_webhook(payload_in_bytes, monnify_hash, request.META):
            return Response(
                {"status": "failed", "message": "Invalid Monnify signature or IP"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            payload = json.loads(payload_in_bytes.decode("utf-8"))
            event_type = payload.get("eventType")

            if event_type != "SUCCESSFUL_TRANSACTION":
                return Response(
                    {"status": "success", "message": "Event not processed"},
                    status=status.HTTP_200_OK
                )

            event_data = payload.get("eventData", {})
            payment_reference = event_data.get("paymentReference")
            amount_paid = Decimal(str(event_data.get("amountPaid", "0")))
            customer_email = event_data.get("customer", {}).get("email")
            account_reference = event_data.get("product", {}).get("reference")

            # Get user
            user = None
            if customer_email:
                try:
                    user = CustomUser.objects.get(email__iexact=customer_email)
                except CustomUser.DoesNotExist:
                    pass
            if not user and account_reference:
                username_part = account_reference.split('_')[-1]
                try:
                    user = CustomUser.objects.get(username__iexact=username_part)
                except CustomUser.DoesNotExist:
                    pass

            if not user:
                return Response(
                    {"status": "success", "message": "User not found"},
                    status=status.HTTP_200_OK,
                )

            if MonnifyTransaction.objects.filter(payment_reference=payment_reference).exists():
                return Response(
                    {"status": "success", "message": "Duplicate webhook"},
                    status=status.HTTP_200_OK,
                )

            # Credit user
            user.balance = (user.balance or Decimal('0.00')) + amount_paid
            user.save()

            # Check and apply first deposit reward
            was_first_deposit = not getattr(user, 'first_deposit_reward_given', True)
            handle_first_deposit_reward(user)

            # Deduct Monnify fee only if this is NOT the first deposit

            # should_deduct_fee = getattr(user, 'first_deposit_reward_given', False)
            # monnify_fee = Decimal(getattr(settings, "MONNIFY_TRANSACTION_FEE", "35.00"))


            # # 🛠️ Skip Monnify fee for first deposit
            # if not was_first_deposit and should_deduct_fee and user.balance >= monnify_fee:
            #     user.balance -= monnify_fee
            #     user.save()

            # Monnify fee = 03% of amount paid
            monnify_fee = amount_paid * Decimal('0.03')

            # Handle Monnify fee
            if was_first_deposit:
                # First deposit: handle fee via custom logic in reward function
                handle_first_deposit_reward(user, amount_paid)
            else:
                # Not first deposit: deduct 03% from balance if user has enough
                if user.balance >= monnify_fee:
                    user.balance -= monnify_fee
                    user.save()

                # Add half of the 3% charge to bonus
                half_bonus = monnify_fee / 2
                user.bonus += half_bonus
                user.save()

            # Log transaction
            MonnifyTransaction.objects.create(
                user=user,
                amount=amount_paid,
                payment_reference=payment_reference,
                monnify_transaction_reference=event_data.get("transactionReference"),
                bank_code=event_data.get("paymentSourceInformation", [{}])[0].get("bankCode", ""),
                account_number=event_data.get("paymentSourceInformation", [{}])[0].get("accountNumber", ""),
                narration=event_data.get("narration", "User Deposit"),
                status='successful',
                currency=event_data.get("currencyCode", "NGN"),
                response_message=payload,
                transaction_type='first_deposit' if was_first_deposit else 'regular_deposit',
                date=now()
            )

            # Send email
            try:
                send_mail(
                    subject="Wallet Credited Successfully",
                    message=f"Hello {user.username},\n\nYour wallet has been credited with {amount_paid:,.2f}.\nNew balance: {user.balance:,.2f}.\n\nThank you!",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
            except Exception as mail_err:
                print(f"🔥 Error sending confirmation email: {mail_err}")

            return Response(
                {"status": "success", "message": "Wallet credited successfully"},
                status=status.HTTP_200_OK
            )

        except json.JSONDecodeError as e:
            return Response({"status": "failed", "message": "Invalid JSON payload"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"🔥 Internal error: {str(e)}")
            print(traceback.format_exc())
            return Response({"status": "error", "message": "Internal processing error"}, status=status.HTTP_200_OK)

@method_decorator(csrf_exempt, name='dispatch')
def verify_paystack_transaction(reference):
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    }
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

@method_decorator(csrf_exempt, name='dispatch')
class PaystackWebhookView(APIView):
    def post(self, request):
        response = HttpResponse(status=200)
        payload = request.body
        secret = settings.PAYSTACK_SECRET_KEY.encode('utf-8')
        signature = request.headers.get('x-paystack-signature')
        computed_hash = hmac.new(secret, payload, hashlib.sha512).hexdigest()

        # Validate signature
        if not hmac.compare_digest(computed_hash, signature):
            return HttpResponseForbidden('Invalid signature')

        # Parse JSON
        event = json.loads(payload)

        if event.get('event') == 'charge.success':
            data = event.get('data', {})
            reference = data.get('reference')

            verified_data = verify_paystack_transaction(reference)
            if not verified_data or verified_data['data'].get('status') != 'success':
                return HttpResponse(status=400)  # Don't process fake or failed transactions
            
            amount_kobo = data.get('amount')
            amount_naira = Decimal(amount_kobo) / 100
            email = data.get('customer', {}).get('email')
            paid_at_str = data.get('paid_at')
            paid_at = parse_datetime(paid_at_str) if paid_at_str else None
            payment_method = data.get('authorization', {}).get('channel')
            currency = data.get('currency', 'NGN')
            status = data.get('status', 'pending')

            # Check if already recorded
            if PaystackTransaction.objects.filter(reference=reference).exists():
                return response  # Already handled

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                send_mail(
                    subject="❗ Paystack Webhook Failed - User Not Found",
                    message=f"A payment with reference {reference} was received but no user with email {email} was found.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=["yourteam@bigsheriffdata.com"],
                )
                return HttpResponse(status=404)

            # Determine transaction type
            was_first_deposit = not user.first_deposit_reward_given

            # Update balance first
            if hasattr(user, 'balance'):
                user.balance += amount_naira
                user.save()

            # Process bonus or apply charges
            if was_first_deposit:
                handle_first_deposit_reward(user, amount_paid=amount_naira)
            else:
                # Calculate 3% charge
                charge = amount_naira * Decimal('0.03')

                if user.balance >= charge:
                    user.balance -= charge
                    user.save()
                else:
                    print(f"User {user.username} has insufficient balance for 3% charge.")

                # Add half of the 3% charge to bonus
                half_bonus = charge / 2
                user.bonus += half_bonus
                user.save()

            # Save the transaction
            PaystackTransaction.objects.create(
                user=user,
                transaction_type='first_deposit' if was_first_deposit else 'regular_deposit',
                reference=reference,
                amount=amount_naira,
                payment_method=payment_method,
                currency=currency,
                status=status,
                paid_at=paid_at,
                response_message=data
            )

            # Send email
            try:
                send_mail(
                    subject="Wallet Credited Successfully",
                    message=f"Hello {user.username},\n\nYour wallet has been credited with {amount_naira:,.2f}.\nNew balance: {user.balance:,.2f}.\n\nThank you!",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
            except Exception as mail_err:
                print(f"🔥 Error sending confirmation email: {mail_err}")

            return Response(
                {"status": "success", "message": "Wallet credited successfully"},
                status=status.HTTP_200_OK
            )

        return response

@method_decorator(csrf_exempt, name='dispatch')
class InitializeTransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = request.data.get('amount')
        if not amount:
            return Response({'error': 'Amount is required'}, status=400)

        try:
            amount_kobo = int(Decimal(amount) * 100)
        except Exception as e:
            return Response({'error': 'Invalid amount format', 'details': str(e)}, status=400)

        email = request.user.email
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "email": email,
            "amount": amount_kobo,
            "callback_url": "http://bigsheriffdata.onrender.com/payment-complete/",
            "metadata": {
                "user_id": request.user.id,
                "purpose": "wallet_funding"
            }
        }

        try:
            res = requests.post("https://api.paystack.co/transaction/initialize", json=payload, headers=headers)
            if res.status_code == 200:
                return Response(res.json(), status=200)
            else:
                return Response({"error": "Paystack initialization failed", "details": res.text}, status=res.status_code)
        except Exception as e:
            return Response({"error": "An unexpected error occurred", "details": str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class PaystackConfigView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'publicKey': settings.PAYSTACK_PUBLIC_KEY,
            'userEmail': request.user.email
        })

@method_decorator(csrf_exempt, name='dispatch')
class PaystackTransactionListView(ListAPIView):
    serializer_class = PaystackTransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return transactions that belong to the authenticated user
        return PaystackTransaction.objects.filter(user=self.request.user).order_by('-created_at')


class BankTransferAPIView(APIView):
    def post(self, request):
        serializer = BankTransferSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user  # The user initiating the transfer
            amount = serializer.validated_data['amount']  # The amount to transfer
            bank_code = serializer.validated_data['bank_code']
            account_number = serializer.validated_data['account_number']
            reference = serializer.validated_data['reference']

            # Calculate the total bonus across all users
            total_bonus = User.objects.aggregate(Sum('bonus'))['bonus__sum'] or 0

            # Prevent duplicate transaction by checking if the reference already exists
            if BankTransfer.objects.filter(reference=reference).exists():
                return Response({
                    "error": "This transaction has already been processed.",
                    "reference": reference
                }, status=status.HTTP_409_CONFLICT)

            # Ensure the amount is valid (less than or equal to the total bonus)
            if amount > total_bonus:
                return Response({"error": "Requested amount exceeds the total available bonus"}, status=status.HTTP_400_BAD_REQUEST)

            # Call Monnify API to transfer the specified amount
            monnify_api = MonnifyBankTransferAPI(
                base_url="https://api.monnify.com",
                auth_token=settings.MONNIFY_CLIENT_ID,
                secret_key=settings.MONNIFY_CLIENT_SECRET
            )

            response = monnify_api.send_bonus_to_platform(
                amount=float(amount),
                bank_code=bank_code,
                account_number=account_number,
                reference=reference
            )

            print("Monnify API Response:", response)

            response_body = response.get("responseBody", {}) if response else {}
            monnify_status = response_body.get("status", "FAILED")
            monnify_ref = response_body.get("reference")
            monnify_msg = response.get("responseMessage", "No response message")
            monnify_success = response.get("requestSuccessful", False)

            # Start saving records
            with db_transaction.atomic():
                # Save bank transfer record
                transfer = BankTransfer.objects.create(
                    user=user,  # Record the initiating user
                    amount=amount,
                    bank_code=bank_code,
                    account_number=account_number,
                    reference=reference,
                    status="completed" if monnify_status in ["SUCCESS", "PENDING_AUTHORIZATION"] else "failed"
                )
                transfer.save()

                # Save monnify transaction record
                transaction = MonnifyTransaction.objects.create(
                    user=user,
                    amount=amount,
                    payment_reference=reference,
                    monnify_transaction_reference=monnify_ref,
                    bank_code=bank_code,
                    account_number=account_number,
                    narration="Partial User Bonus Withdrawal",
                    status=monnify_status,
                    currency="NGN",
                    response_message=response
                )

                # Deduct the bonus proportionally from each user's bonus
                if monnify_status in ["SUCCESS", "PENDING_AUTHORIZATION"] and monnify_success:
                    # Loop through all users and proportionally deduct from each user's bonus
                    for u in User.objects.all():
                        # Calculate the percentage of the total bonus for each user
                        user_share = u.bonus / total_bonus if total_bonus else 0

                        # Proportional deduction
                        deduction = amount * user_share

                        # Reduce the user's bonus by the proportional amount
                        u.bonus -= deduction
                        u.save()

                    transaction.save()

            if monnify_status in ["SUCCESS", "PENDING_AUTHORIZATION"] and monnify_success:
                return Response({
                    "message": f"Transfer of {amount} initiated successfully ({monnify_status})",
                    "reference": reference,
                    "monnify_status": monnify_status
                }, status=status.HTTP_200_OK)
            else:
                transaction.save()
                return Response({
                    "message": "Transfer failed",
                    "monnify_status": monnify_status,
                    "response_message": monnify_msg,
                    "reference": reference
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BuyAirtimeView(APIView):

    NETWORK_MAP = {
        1: 'MTN',
        2: 'GLO',
        3: 'ETISALAT',
        4: 'AIRTEL'
    }

    def post(self, request, *args, **kwargs):
        # Ensure the user is logged in
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

        # Add the user to the request data (automatically set the logged-in user as the 'user')
        request.data['user'] = request.user.id

        # Create the serializer instance with the request data
        serializer = BuyAirtimeSerializer(data=request.data)

        # Get the 'amount' from the request data
        amount = request.data.get('amount')

        if amount is None:
            return JsonResponse({'status': 'error', 'message': 'Amount is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user has enough balance
        if request.user.balance < float(amount):
            raise ValidationError({"detail": "Insufficient balance to complete the purchase."})

        # Check if the data is valid
        if serializer.is_valid():
            try:
                # Save the airtime purchase and handle the balance deduction
                airtime_purchase = serializer.save()

                # Calculate the remaining balance from the user’s balance
                remaining_balance = airtime_purchase.user.balance

                # Generate a unique request_id for this transaction
                request_id = self.generate_request_id()

                # Get the network integer from the request
                network_id = int(request.data.get('network', 0))

                # Map the network ID to the corresponding network string
                network = self.NETWORK_MAP.get(network_id, None)

                if not network:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Invalid network. Valid options are: MTN, GLO, AIRTEL, ETISALAT'
                    }, status=status.HTTP_400_BAD_REQUEST)

                # Call the VTPassAPI to process the airtime purchase
                api = VTPassAPI(
                    base_url="https://sandbox.vtpass.com",
                    auth_token = settings.VTPASS_AUTH_TOKEN,
                    secret_key = settings.VTPASS_SECRET_KEY
                )

                # Prepare data for VTPassAPI
                api_data = {
                    'request_id': request_id,  # Include the generated request_id
                    'serviceID': network,  # Use the network string (e.g., MTN)
                    'amount': amount,
                    'phone': request.data.get('mobile_number'),
                }

                # Call the API and get the full transaction response
                response = api.buy_airtime(api_data)

                # Log the raw response for debugging
                print(f"Raw response from VTPass: {response}")

                # Check if the response is valid (not None)
                if response:
                    # Extract details from the response
                    transactions = response.get('content', {}).get('transactions', {})
                    transaction_status = transactions.get('status', 'failed')
                    transaction_id = response.get("requestId", 'N/A')
                    product_name = transactions.get('product_name', 'Unknown Product')

                    # Extract phone and unit price
                    phone_number = transactions.get('unique_element', 'None')
                    unit_price = transactions.get('unit_price', 0)

                    # Save the API response into airtime_response field
                    airtime_purchase.airtime_response = response  # Save the full response
                    airtime_purchase.transaction_id = response.get("requestId", 'N/A')
                    

                    # Handle transaction status
                    if transaction_status == 'failed':
                        airtime_purchase.save()
                        print(f"Transaction failed with transaction ID: {transaction_id}")
                        return self.handle_failed_transaction(transaction_id, response)

                    # If successful, save the transaction and return response
                    elif transaction_status == 'delivered':
                        airtime_purchase.status = 'completed'
                        # Extract commission from the API response
                        commission = response.get("content", {}).get("transactions", {}).get("commission", 0)

                        # Ensure commission is a Decimal (convert if it's a float)
                        commission = Decimal(commission)

                        # Save the commission in the user's bonus field
                        user = request.user  # Assuming the airtime_purchase has a 'user' field
                        user.bonus += commission  # Add the commission to the current bonus
                        user.save()  # Save the updated bonus field

                        # Deduct balance and save the successful transaction
                        request.user.balance -= Decimal(str(amount))
                        request.user.save()

                        Transaction.objects.create(
                            user=request.user,
                            transaction_type='Airtime purchase',
                            amount=amount,
                            status='completed',
                            product_name=product_name,
                            transaction_id=transaction_id,
                            unique_element=phone_number,
                            unit_price=unit_price,
                        )

                        airtime_purchase.save()  # Ensure the purchase is saved after updating the response

                        return Response({
                            'status': 'success',
                            'remaining_balance': str(remaining_balance),
                            'transaction_id': transaction_id,
                            'product_name': product_name,
                            'phone': phone_number,
                            'unit_price': unit_price
                        }, status=status.HTTP_200_OK)

                    else:
                        print(f"Unexpected response from VTPass: {response}")
                        return Response({
                            'status': 'error',
                            'message': 'Transaction failed. Please check the details or try again.',
                            'response': response
                        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


                else:
                    # If no response or invalid response from VTPass
                    print("Invalid or empty response from VTPass.")
                    return Response({
                        'status': 'error',
                        'message': 'Invalid response from VTPass. Please try again.',
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            except Exception as e:
                # Handle unexpected errors during the purchase process
                print(f"Unexpected error: {str(e)}")
                return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            # Print validation errors
            print(f"Validation errors: {serializer.errors}")
            return Response({
                'status': 'error',
                'errors': serializer.errors  # Return serializer validation errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def generate_request_id(self):
        """Generate a unique request ID using timestamp and UUID"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        unique_id = uuid.uuid4().hex
        return f"{timestamp}_{unique_id}"

    def handle_failed_transaction(self, transaction_id, api_response):
        """Handle failed transaction and log it"""
        # print(f"Transaction failed with transaction ID: {transaction_id}")
        # print(f"API Response: {api_response}")

        # Check for the specific error code
        if api_response.get("code") == "017":
            message = "The amount exceeds the maximum allowed for this transaction."
        else:
            message = "An unknown error occurred during the transaction."

        # Extract data from the API response
        transactions = api_response.get('content', {}).get('transactions', {})
        product_name = transactions.get('product_name', 'Unknown Product')
        phone_number = transactions.get('unique_element', '')  # Get the phone number from unique_element
        unit_price = transactions.get('unit_price', 0)  # Get the unit price

        # Create and save the failed transaction in the database
        Transaction.objects.create(
            user=self.request.user,
            transaction_type='Airtime Purchase',
            amount=self.request.data.get('amount'),
            status='failed',
            product_name=product_name,
            transaction_id=transaction_id,  # Save the transaction ID
            unique_element=phone_number,  # Save the phone number from unique_element
            unit_price=unit_price,  # Save the unit price from the response
        )

        return Response({
            'status': 'failed',
            'message': "Transaction failed with an external API.",
            'transaction_id': transaction_id,
            'response': api_response  # For debugging purposes
        }, status=status.HTTP_200_OK)




class BuyDataAPIView(APIView):
    permission_classes = [IsAuthenticated]
    NETWORK_MAP = {
        1: 'MTN',
        2: 'GLO',
        3: 'ETISALAT',
        4: 'AIRTEL'
    }

    def post(self, request, *args, **kwargs):
        """
        Create a new BuyData record, process the purchase, and call the external API to complete the transaction.
        """
        # Serialize the input data
        serializer = BuyDataSerializer(data=request.data)

        if serializer.is_valid():
            try:
                with db_transaction.atomic():
                    # Extract the amount and convert to Decimal
                    amount = serializer.validated_data.get('amount', 0)
                    amount_decimal = Decimal(str(amount))  

                    # Check if the user has enough balance
                    if request.user.balance < amount_decimal:
                        raise ValidationError({"detail": "Insufficient balance to complete this purchase."})

                    # Save the BuyData instance (no deduction yet)
                    buy_data_instance = serializer.save()

                    # Create a transaction for this data purchase (even before calling external API)
                    transaction = Transaction.objects.create(
                        user=request.user,
                        transaction_type='Data Purchase',
                        amount=buy_data_instance.amount,
                        status='pending',  # Mark as pending initially
                        description=f"Data purchase for {buy_data_instance.data_plan}",
                        product_name=self.NETWORK_MAP.get(buy_data_instance.network, ""),  # Set the network as product_name
                        unit_price=buy_data_instance.amount,  # Set the unit_price to the amount
                        unique_element=buy_data_instance.mobile_number,
                        transaction_id=None,
                    )

                    # Deduct balance from user account using process_purchase
                    user = buy_data_instance.process_purchase()  # Deduct balance only once
                    remaining_balance = user.balance

                    # Log the balance after deduction
                    print(f"Balance after deduction: {remaining_balance}")

                    # Validate the network
                    network_id = int(request.data.get('network', 0))
                    network = self.NETWORK_MAP.get(network_id, None)

                    if not network:
                        return JsonResponse({
                            'status': 'error',
                            'message': 'Invalid network. Valid options are: MTN, GLO, AIRTEL, ETISALAT'
                        }, status=status.HTTP_400_BAD_REQUEST)

                    # Get data plan and validate
                    data_plan = request.data.get('data_plan', None)
                    if not data_plan:
                        return JsonResponse({
                            'status': 'error',
                            'message': 'Data plan not provided.'
                        }, status=status.HTTP_400_BAD_REQUEST)

                    # Call external API for the purchase
                    api_response, service_variations = self.call_external_api(buy_data_instance, network, data_plan)

                    # Save the API response in the data_response field
                    buy_data_instance.data_response = api_response
                    buy_data_instance.transaction_id = api_response.get("requestId", 'N/A')

                    transaction.transaction_id = api_response.get("requestId", 'N/A')

                    if api_response.get("content", {}).get("transactions", {}).get("status") == "delivered":
                        # Deduct balance and save the successful transaction
                        request.user.balance -= Decimal(str(amount))
                        request.user.save()

                        # Extract commission from the API response
                        commission = api_response.get("content", {}).get("transactions", {}).get("commission", 0)

                        # Ensure commission is a Decimal (convert if it's a float)
                        commission = Decimal(commission)

                        # Add ₦10 extra bonus
                        bonus_to_add = commission + Decimal('10')

                        # Save the commission in the user's bonus field
                        user = request.user  # Assuming the buy_data_instance has a 'user' field
                        user.bonus += bonus_to_add  # Add the commission to the current bonus
                        user.save()  # Save the updated bonus field

                        buy_data_instance.status = 'completed'
                        buy_data_instance.save()

                        # If API call is successful, mark transaction as completed
                        transaction.status = 'completed'
                        transaction.save()

                        return Response({
                            'message': 'Data purchase successful!',
                            'remaining_balance': str(remaining_balance),
                            'service_variations': service_variations
                        }, status=status.HTTP_201_CREATED)

                    else:
                        # If API call fails, log the failure and revert the user's balance
                        print(f"API failed, reverting balance. Original user balance: {remaining_balance}, Deducted amount: {amount_decimal}")

                        # Revert the balance by adding the deducted amount back
                        user.balance += amount_decimal  # Revert the balance deduction
                        user.save()  # Save the user after reversion

                        # Mark BuyData as failed
                        buy_data_instance.status = 'failed'
                        buy_data_instance.save()

                        # Mark the transaction as failed
                        transaction.status = 'failed'
                        transaction.save()

                        # Log the updated balance after reversion
                        print(f"Balance after reversion: {user.balance}")

                        # Return error response
                        return Response({
                            'error': 'Transaction failed with an external API.',
                            'remaining_balance': str(remaining_balance),
                            'details': api_response
                        }, status=status.HTTP_200_OK)

            except ValidationError as e:
                # Handle the exception and ensure balance reversion occurs
                print(f"Error during transaction: {e}")
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    def call_external_api(self, buy_data_instance, network, data_plan):
        """ Helper method to call the external API for purchasing data and fetching service variations. """
        base_url = "https://sandbox.vtpass.com"
        auth_token = settings.VTPASS_AUTH_TOKEN,
        secret_key = settings.VTPASS_SECRET_KEY
        api = VTPassDataAPI(base_url, auth_token, secret_key)

        # Generate unique request ID
        date_time_format = datetime.now().strftime("%Y%m%d%H%M%S")
        request_id = str(date_time_format) + create_random_id()

        # Get the network name from the NETWORK_MAP
        network_name = self.NETWORK_MAP.get(buy_data_instance.network, "").lower()

        if not network_name:
            raise ValidationError(f"Invalid network ID: {buy_data_instance.network}")

        # Handle ETISALAT-specific condition first
        if network_name == "etisalat" and "sme" in data_plan.lower():
            network_name = "9mobile-sme"  # Change network name to 9mobile-sme if the condition is met
            print(f"Modified network for service variation (ETISALAT + SME): {network_name}")  # Debugging line
        else:
            # For all other networks, check if 'SME' is in data_plan
            if "sme" in data_plan.lower():
                network_name += "-sme"  # Append '-sme' to the network name for SME plans
                print(f"Modified network for service variation (SME): {network_name}")  # Debugging line
            else:
                print(f"Network for service variation: {network_name}")  # Debugging line

        # Fetch service variations from external API
        service_variations_response = api.fetch_service_variations(network_name)

        # Parse the response to get variations
        try:
            service_variations = json.loads(service_variations_response)
        except json.JSONDecodeError:
            raise ValidationError("Failed to decode the service variations response. Response was not valid JSON.")

        selected_variation_code = None

        if service_variations.get("response_description") == "000":
            variations = service_variations["content"]["varations"]
            # Loop through variations to find the selected data plan
            for variation in variations:
                if variation["name"].lower() == data_plan.lower():
                    selected_variation_code = variation["variation_code"]
                    break

        if not selected_variation_code:
            raise ValidationError(f"Variation for the selected data plan '{data_plan}' not found.")

        # Prepare the data for the external API request
        request_data = {
            'request_id': request_id,
            "billerCode": "07046799872",  # Example biller code
            "variation_code": selected_variation_code,
            "phone": buy_data_instance.mobile_number
        }

        # Check if the data_plan contains 'SME' (case-insensitive)
        if "sme" in data_plan.lower():  # If data_plan contains 'sme' (case-insensitive)
            request_data["serviceID"] = f"{network_name}-sme"  # Modify serviceID for SME data
        else:
            request_data["serviceID"] = f"{network_name}-data"  # Default for other data plans

        # Call the external API to make the purchase
        api_response = api.buy_data(request_data)

        return api_response, service_variations



# Helper function to create random ID
def create_random_id():
    num = random.randint(1000, 4999)
    num_2 = random.randint(5000, 8000)
    num_3 = random.randint(111, 999) * 2
    return str(num) + str(num_2) + str(num_3) + str(uuid.uuid4())



class TVServiceAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def post(self, request, *args, **kwargs):
        """
        Create a new TV service subscription and process the purchase.
        """
        # Directly access the data fields from request.data
        billers_code = request.data.get('billersCode', None)
        service_id = request.data.get('serviceID', None)
        if service_id:
            service_id = service_id.lower()


        # Log request data for debugging purposes
        print("Request Data:", request.data)
        print(f"Billers Code: {billers_code}, Service ID: {service_id}")

        action = request.data.get('action', None)
        type_field = request.data.get('type', None)  # Fetch the 'type' field

        # If action is 'change', proceed to bouquet change
        if action == 'change' or type_field is not None:
            bouquet_code = request.data.get('bouquet', None)
            smartcard_number = billers_code
            phone_number = request.data.get('phone_number', None)
            amount = request.data.get('amount', None)

            # Ensure required fields are present
            # if not bouquet_code or not smartcard_number or not phone_number:
            #     return Response({"error": "Missing bouquet, smartcard number, or phone number."}, status=status.HTTP_400_BAD_REQUEST)

            # Check if user has sufficient balance
            if request.user.balance < Decimal(str(amount)):
                return Response({"error": "Insufficient balance to proceed with this transaction."}, status=status.HTTP_400_BAD_REQUEST)

            # Deduct the amount from user's balance
            request.user.balance -= Decimal(str(amount))
            request.user.save()

            # Create the transaction record before making the API call
            transaction = Transaction.objects.create(
                user=request.user,
                transaction_type='TV Subscription',
                amount=Decimal(str(amount)),
                description=f"TV Subscription for bouquet {bouquet_code}",
                status="Pending",  # Mark as "Pending" initially
                product_name=service_id,
                unique_element=smartcard_number,
                unit_price=Decimal(str(amount)),
                transaction_id=None,
            )

            # Instantiate API class
            api = VTPassTVSubscription(
                base_url="https://sandbox.vtpass.com", 
                auth_token = settings.VTPASS_AUTH_TOKEN,
                secret_key = settings.VTPASS_SECRET_KEY  # Replace with your actual secret key
            )

            # Fetch service variations
            fetch_service_variations = api.fetch_service_variations(service_id)
            print("Fetch Service Variations Response Type:", type(fetch_service_variations))
            # print("Fetch Service Variations Response:", fetch_service_variations)

            # If the response is a string, parse it as JSON
            if isinstance(fetch_service_variations, str):
                fetch_service_variations = json.loads(fetch_service_variations)

            # print("Parsed Service Variations:", fetch_service_variations)

            if not fetch_service_variations or fetch_service_variations.get('response_description') != '000':
                return Response({"error": "Failed to fetch service variations."}, status=status.HTTP_400_BAD_REQUEST)

            # Find the variation_code based on the provided amount
            variation_code = None
            for variation in fetch_service_variations.get('content', {}).get('variations', []):
                if float(variation.get('variation_amount', 0)) == float(amount):
                    variation_code = variation.get('variation_code')
                    break

            # If no matching variation is found, return an error
            if not variation_code:
                return Response({"error": "No matching variation found for the provided amount."}, status=status.HTTP_400_BAD_REQUEST)

            # Prepare bouquet payload with the correct variation_code
            bouquet_payload = {
                'request_id': str(datetime.now().strftime("%Y%m%d%H%M%S")) + create_random_id(),
                "serviceID": service_id,
                "billersCode": smartcard_number,
                "variation_code": variation_code,  # Use the dynamic variation_code
                'amount': amount,
                "phone": phone_number,
            }

            # Call bouquet change API
            bouquet_change_result = api.bouquet_change(bouquet_payload)

             # Save the API response in the transaction's `data_response` field
            transaction.data_response = bouquet_change_result  # Save the response here
            transaction.transaction_id = bouquet_change_result.get("requestId", 'N/A')

            # Regardless of transaction success, create the TVService instance
            tv_service = TVService.objects.create(
                user=request.user,
                tv_service=service_id,  # For example, assuming the service is DSTV (replace with actual logic)
                action="change",
                bouquet=bouquet_code,
                amount=Decimal(str(amount)),
                smartcard_number=smartcard_number,
                phone_number=phone_number,
                data_response=bouquet_change_result,  # Save the response
                transaction_id=None,
            )

            tv_service.transaction_id = bouquet_change_result.get("requestId", 'N/A')
            tv_service.save()  # Don't forget to save it

             # Check if the transaction was successful based on the response
            if bouquet_change_result and bouquet_change_result.get('code') == '000':
                # Extract necessary details from the JSON response
                transaction_data = bouquet_change_result.get('content', {}).get('transactions', {})
                                                                                
                # Check if the transaction status is 'delivered'
                if transaction_data.get('status') == 'delivered':

                    # Extract commission from the API response
                    commission = bouquet_change_result.get("content", {}).get("transactions", {}).get("commission", 0)

                    # Ensure commission is a Decimal (convert if it's a float)
                    commission = Decimal(commission)

                    # Save the commission in the user's bonus field
                    user = request.user  # Assuming the bouquet_change_result has a 'user' field
                    user.bonus += commission  # Add the commission to the current bonus
                    user.save()  # Save the updated bonus field

                    # Mark the transaction as completed
                    transaction.status = 'completed'
                    transaction.transaction_id = transaction_data.get("transactionId", 'N/A')
                    transaction.save()

                    # Return success response with the relevant details
                    return Response({
                        "success": True,
                        "message": "Bouquet change successful!",
                        "transactionId": transaction_data.get("transactionId"),
                        "amount": transaction_data.get("amount"),
                        "status": transaction_data.get("status"),
                        "details": bouquet_change_result.get("response_description"),
                    }, status=status.HTTP_200_OK)
                else:
                    # If the API response indicates failure, refund the deducted amount and mark the transaction as failed
                    refund_amount = bouquet_change_result.get('amount', '0.00')
                    request.user.balance += Decimal(str(refund_amount))
                    request.user.save()

                    # Update transaction status to 'Failed'
                    transaction.status = 'Failed'
                    transaction.save()

                    # Return failure response with the refund and error message
                    return Response({
                        "success": False,
                        "error": "Bouquet change failed. Refund issued.",
                        "transactionId": transaction_data.get("transactionId"),
                        "amount": transaction_data.get("amount"),
                        "status": transaction_data.get("status"),
                        "details": bouquet_change_result.get("response_description"),
                    }, status=status.HTTP_200_OK)


        # Handle other actions like 'renew' (this part is kept intact)
        # elif action == 'renew' or type_field is not None:
        #     # If action is 'renew', you can implement the renew logic here
        #     return Response({"message": "Service Not Available at the moment"}, status=status.HTTP_200_OK)

        # Ensure that we have the full and correct values
        # Get the raw values from request data
        billers_code = request.data.get('billersCode', '').strip()
        phone_number = request.data.get('phone_number', '').strip()
        service_id = request.data.get('serviceID', '').strip().lower()

        # Use phone number as fallback if billers code is not provided
        if not billers_code:
            billers_code = phone_number

        # Ensure that we have the required values before proceeding
        if billers_code and service_id:
            service_data = {
                "billersCode": billers_code,
                "serviceID": service_id
            }

            # Log final service data
            print("Service Data for Verification:", service_data)


        # Ensure that billers_code is not None before trying to strip
        # if billers_code:
        #     billers_code = billers_code.strip()
        # else:
        #     return Response({"error": "Billers code is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure service_id is not None before trying to strip
        if service_id:
            service_id = service_id.strip().lower()
        else:
            return Response({"error": "Service ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Now let's create the serializer data
        data = {
            "billersCode": billers_code.strip(),
            "serviceID": service_id.strip().lower()
        }

        # Pass the request context to the serializer to access the authenticated user
        serializer = TVServiceSerializer(data=data, context={'request': request})

        # print('Request serializer:', serializer)

        if serializer.is_valid():
            try:
                # Instantiate VTPassTVSubscription API class
                api = VTPassTVSubscription(
                    base_url="https://sandbox.vtpass.com", 
                    auth_token = settings.VTPASS_AUTH_TOKEN,
                    secret_key = settings.VTPASS_SECRET_KEY  # Replace with your actual secret key
                )

                # Log the final service_data for verification
                # print("Service Data for Verification: ", service_data)

                # Call the verify_smartCard_number method with the correct data
                verify_result = api.verify_smartCard_number(service_data)

                # Check if the result is valid and if the status is 'Open'
                if verify_result:
                    # Check if there is an error in the content
                    content = verify_result.get('content', {})
                     # If content is a string, wrap it in a dict with 'error' key
                    if isinstance(content, str):
                        return Response({
                            "valid": False,
                            "message": content,
                            "content": {"error": content}
                        }, status=status.HTTP_200_OK)

                    # If content is a dict, continue as expected
                    if content.get('error'):
                        return Response({
                            "valid": False,
                            "message": content.get('error'),
                            "content": content
                        }, status=status.HTTP_200_OK)

                    # Success case
                    return Response({
                        "valid": True,
                        "message": "Validation successful.",
                        "content": content
                    }, status=status.HTTP_200_OK)


            except ValidationError as e:
                # Handle errors during the purchase processing (e.g., insufficient funds)
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        # Return validation errors from the serializer
        if not serializer.is_valid():
            return Response({"error": "Validation failed", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ElectricityBillCreateView(APIView):
    permission_classes = [IsAuthenticated] 
    """
    API View for creating an Electricity Bill, deducting user balance, and creating a corresponding transaction.
    """

    def post(self, request, *args, **kwargs):
        """
        Handle POST request to create an electricity bill, validate balance, and process transaction.
        """

        meter_number = request.data.get('meter_number')
        service_id = request.data.get('serviceID')
        meter_type = request.data.get('meter_type')
        phone = request.data.get('phone_number')
        amount = request.data.get('amount')
    
        # Ensure that we have the full and correct values
        if meter_number and service_id and meter_type:
            # If data exists, strip whitespaces and process
            data = {
                "billersCode": meter_number.strip(),
                "serviceID": service_id.strip().lower(),
                'type': meter_type.strip().lower()
            }

            # Log final data
            print("Service Data for Verification:", data)
        

        # Ensure that billers_code is not None before trying to strip
        if meter_number:
            meter_number = meter_number.strip()
        else:
            return Response({"error": "Meter Number is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure service_id is not None before trying to strip
        if service_id:
            service_id = service_id.strip().lower()
        else:
            return Response({"error": "Service ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        if meter_type:
            meter_type = meter_type.strip().lower()
        else:
            return Response({"error": "Meter Type is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Now let's create the serializer data
        data = {
            "billersCode": meter_number.strip(),
            "serviceID": service_id.strip().lower(),
            'type': meter_type.strip().lower()
        }
       
        # Initialize the serializer with the request data
        serializer = ElectricityBillSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            try:
                with db_transaction.atomic():
                    # Extract the amount from the validated data
                    amount = serializer.validated_data.get('amount', 0)
                    amount_decimal = Decimal(str(amount))  # Convert to Decimal

                    # Check if the user has enough balance
                    if request.user.balance < amount_decimal:
                        raise ValidationError({"detail": "Insufficient balance to complete this purchase."})

                    # Save the ElectricityBill instance (without deducting balance yet)
                    Electricity_Bill = serializer.save(user=request.user)

                    # Create a transaction for the electricity bill purchase (status 'pending' initially)
                    transaction = Transaction.objects.create(
                        user=request.user,
                        transaction_type='Electricity Bill',
                        amount=Decimal(str(amount)),
                        status='pending',  # Pending status initially
                        description=f"Payment for electricity bill with Meter Number {Electricity_Bill.meter_number}",
                        product_name=Electricity_Bill.serviceID,
                        unique_element=Electricity_Bill.meter_number,
                        transaction_id=None
                    )

                    # Deduct balance from the user's account
                    user = Electricity_Bill.process_purchase()  # This handles balance deduction

                    remaining_balance = user.balance
                    print(f"Balance after deduction: {remaining_balance}")

                    api = VTPassElectricity(
                        base_url="https://sandbox.vtpass.com",
                        auth_token = settings.VTPASS_AUTH_TOKEN,
                        secret_key = settings.VTPASS_SECRET_KEY # Replace with your actual secret key
                    )

                    # Convert Decimal to float or string for JSON serialization
                    amount = float(amount_decimal)  # Or str(amount_decimal)
                    date_time_format = Mdate.now().strftime("%Y%m%d%H%M%S")
                    payload = {
                        'request_id': str(date_time_format) + create_random_id(),
                        "serviceID": service_id,
                        "billersCode": meter_number,
                        "variation_code": meter_type,
                        'amount': amount,
                        "phone": phone 
                    }

                    Meter_payment = api.Meter_payment(payload)

                    transaction.transaction_id = Meter_payment.get("requestId", 'N/A')

                    # Regardless of transaction success, create the TVService instance
                    electricity_bill = ElectricityBill.objects.create(
                        user=request.user,
                        serviceID=service_id,  # For example, assuming the service is DSTV (replace with actual logic)
                        meter_number=meter_number,
                        amount=Decimal(str(amount)),
                        meter_type= meter_type,
                        phone_number=phone,
                        data_response=Meter_payment,  # Save the response
                        transaction_id=None,
                    )

                    electricity_bill.transaction_id = Meter_payment.get("requestId", 'N/A')
                    electricity_bill.save()  # Don't forget to save it

                    user=request.user
                    
                    if Meter_payment.get("content", {}).get("transactions", {}).get("status") == "delivered":

                        # If the API response is successful, mark the transaction as completed
                        transaction.status = 'completed'
                        transaction.save()
                        
                         # Extract commission from the API response
                        commission = Meter_payment.get("content", {}).get("transactions", {}).get("commission", 0)

                        # Ensure commission is a Decimal (convert if it's a float)
                        commission = Decimal(commission)

                        # Save the commission in the user's bonus field
                        user = user = request.user  # Assuming the Meter_payment has a 'user' field
                        user.bonus += commission  # Add the commission to the current bonus
                        user.save()  # Save the updated bonus field

                        # Return success response with remaining balance and other details
                        return Response({
                            'success': True,
                            'message': 'Electricity bill payment successful!',
                            'remaining_balance': str(remaining_balance),
                            'transaction_id': transaction.transaction_id,
                            "content": Meter_payment
                        }, status=status.HTTP_201_CREATED)

                    else:
                        # If the API fails, log the failure and revert the balance
                        print(f"API failed, reverting balance. Original user balance: {remaining_balance}, Deducted amount: {amount_decimal}")

                        # Revert the deducted balance
                        refund_amount = Meter_payment.get('amount', '0.00')
                        user.balance += amount_decimal
                        user.save()

                        # Mark the transaction as failed
                        transaction.status = 'failed'
                        transaction.save()

                        print(f"Balance after reversion: {user.balance}")

                        # Return error response due to API failure
                        return Response({
                            'success': False,
                            'error': 'Transaction failed with the external API.',
                            'details':Meter_payment,
                            'message': Meter_payment.get("response_description"),
                            'refund_amount': refund_amount,
                            'transaction_id': Meter_payment.get("requestId")
                        }, status=status.HTTP_200_OK)

            except ValidationError as e:
                # Handle validation error and ensure balance reversion happens if necessary
                print(f"Error during transaction: {e}")
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
        try:
            # Call the VTPass API to verify the meter number
            api = VTPassElectricity(
                base_url="https://sandbox.vtpass.com",
                auth_token = settings.VTPASS_AUTH_TOKEN,
                secret_key = settings.VTPASS_SECRET_KEY  # Replace with your actual secret key
            )
            verify_result = api.verify_meter_number(data)

            # Check if the result is valid and if the status is 'Open'
            if verify_result:
                # Check if there is an error in the content
                content = verify_result.get('content', {})
                if content.get('error'):
                    return Response({
                        "valid": False,
                        "message": content.get('error'),  # Show the error message from the content
                        "content": content
                    }, status=status.HTTP_200_OK)
                else:
                    # If there is no error, return a successful response
                    return Response({
                        "valid": True,
                        "message": "Validation successful.",
                        "content": content
                    }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "valid": False,
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class WaecPinGeneratorCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        serviceID = request.data.get('serviceID')
        exam_type = request.data.get('ExamType')
        phone_number = request.data.get('phone_number')
        quantity = request.data.get('quantity')
        amount = request.data.get('amount')

        print(f"Received data: {request.data}")

        service_name = request.data.get('serviceID')

        data = request.data.dict()  # Convert QueryDict to regular dict
        serializer = WaecPinGeneratorSerializer(data=data, context={'request': request})

        if serializer.is_valid():
            try:
                with db_transaction.atomic():
                    # Now perform internal validation for quantity and amount
                    if quantity is None or amount is None:
                        return Response({"error": "Quantity and amount are required."}, status=status.HTTP_400_BAD_REQUEST)

                    # Validate that quantity is a positive integer
                    try:
                        quantity = int(quantity)
                        if quantity <= 0:
                            raise ValidationError("Quantity must be a positive integer.")
                    except ValueError:
                        return Response({"error": "Quantity must be a valid integer."}, status=status.HTTP_400_BAD_REQUEST)

                    # Validate that amount is a positive value
                    try:
                        amount = Decimal(str(amount))
                        if amount <= 0:
                            raise ValidationError("Amount must be a positive value.")
                    except ValueError:
                        return Response({"error": "Amount must be a valid number."}, status=status.HTTP_400_BAD_REQUEST)
                    # Check if the user has enough balance (assuming the user has a balance field)
                    user_balance = request.user.balance

                    total_amount = Decimal(amount) * int(quantity)  # Total amount for the requested quantity of pins
                    if user_balance < total_amount:
                        raise ValidationError({"detail": "Insufficient balance to complete this transaction."})

                    # Create the WaecPinGenerator instance
                    waec_pin_generator = serializer.save(user=request.user)

                    # Process the transaction (create a transaction record)
                    transaction = Transaction.objects.create(
                        user=request.user,
                        transaction_type='Waec Pin Generation',
                        amount=total_amount,
                        status='pending',  # Pending status initially
                        description=f"Payment for {quantity} WAEC pins generation.",
                        product_name=waec_pin_generator.ExamType,
                        unique_element=waec_pin_generator.phone_number,
                        transaction_id=None
                    )

                    # Deduct balance from the user's account (assuming process_purchase handles this)
                    request.user = waec_pin_generator.process_purchase()
                    request.user.save()

                    remaining_balance = request.user.balance
                    print(f"Balance after deduction: {remaining_balance}")

                    date_time_format = Mdate.now().strftime("%Y%m%d%H%M%S")
                    data = {
                        'request_id': str(date_time_format) + create_random_id(),
                        "serviceID": serviceID,
                        "variation_code": "waec-registraion",
                        "quantity": quantity,
                        "phone": phone_number
                    }

                    # Call he Waec_Registration_pin API
                    api = VTPassEducationAPI(
                        base_url="https://sandbox.vtpass.com",
                        auth_token = settings.VTPASS_AUTH_TOKEN,
                        secret_key = settings.VTPASS_SECRET_KEY  # Replace with your actual secret key
                    )
                    Waec_Registration_pin = api.Waec_Registration_pin(data)

                    transaction.transaction_id = Waec_Registration_pin.get("requestId", 'N/A')

                    # Regardless of transaction success, create the TVService instance
                    Waec_Pin_Generator = WaecPinGenerator.objects.create(
                        user=request.user,
                        serviceID=serviceID,
                        ExamType=exam_type,
                        amount=Decimal(str(amount)),
                        phone_number=phone_number,
                        quantity=quantity,
                        data_response=Waec_Registration_pin,  # Save the response
                        transaction_id=None,
                    )

                    Waec_Pin_Generator.transaction_id = Waec_Registration_pin.get("requestId", 'N/A')
                    Waec_Pin_Generator.save()  # Don't forget to save it

                    # Serialize the WaecPinGenerator instance
                    waec_pin_generator_data = WaecPinGeneratorSerializer(waec_pin_generator).data

                    # Get the user from the request (Django's authenticated user)
                    user = request.user

                    transaction_status = Waec_Registration_pin.get("content", {}).get("transactions", {}).get("status")
                    print(f"API Response Status: {transaction_status}")

                    if transaction_status == "delivered":
                        commission = Waec_Registration_pin.get("content", {}).get("transactions", {}).get("commission", 0)
                        commission = Decimal(commission)
                        user.bonus += commission
                        user.save()

                        transaction.status = 'completed'
                        transaction.save()
                        print(f"Transaction status updated to: {transaction.status}")


                        # Return success response with remaining balance and other details
                        return Response({
                            'success': True,
                            'message': f'{quantity} WAEC pin(s) generated successfully.',
                            'remaining_balance': str(remaining_balance),
                            'transaction_id': transaction.transaction_id,
                            'data': waec_pin_generator_data,
                            "content": Waec_Registration_pin
                        }, status=status.HTTP_201_CREATED)

                    else:
                        # If the API fails, log the failure and revert the balance
                        print(f"API failed, reverting balance. Original user balance: {remaining_balance}, Deducted amount: {amount_decimal}")

                        # Revert the deducted balance
                        refund_amount = Waec_Registration_pin.get('amount', '0.00')
                        user.balance += total_amount
                        user.save()

                        # Mark the transaction as failed
                        transaction.status = 'failed'
                        transaction.save()

                        print(f"Balance after reversion: {user.balance}")

                        # Return error response due to API failure
                        return Response({
                            'success': False,
                            'error': 'Transaction failed with the external API.',
                            'details':Waec_Registration_pin,
                            'message': Waec_Registration_pin.get("response_description"),
                            'refund_amount': refund_amount,
                            'transaction_id': Waec_Registration_pin.get("requestId")
                        }, status=status.HTTP_200_OK)

            except ValidationError as e:
                # Handle validation error
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
        # if not serializer.is_valid():
        #     print("Serializer errors:", serializer.errors)  # This will give more insight into what is failing.
        #     return Response({"error": "Invalid data provided.", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        elif exam_type != '' and not phone_number and not quantity and not amount:
            try:
                # Call the VTPass API to verify the exam type
                api = VTPassEducationAPI(
                    base_url="https://sandbox.vtpass.com",
                    auth_token = settings.VTPASS_AUTH_TOKEN,
                    secret_key = settings.VTPASS_SECRET_KEY  # Replace with your actual secret key
                )
                get_variation_code = api.fetch_service_variations(service_name)

                # Check if the response is valid and parse it as JSON if needed
                if isinstance(get_variation_code, str):  # If the response is a string, parse it as JSON
                    get_variation_code = json.loads(get_variation_code)  # Assuming `json` is imported

                # Now we can safely access the 'content' field
                if get_variation_code:
                    content = get_variation_code.get('content', {})
                    if content.get('error'):
                        return Response({
                            "valid": False,
                            "message": content.get('error'),  # Show the error message from the content
                            "content": content
                        }, status=status.HTTP_200_OK)
                    else:
                        variations = content.get('variations', [])
                        if variations:
                            # Assume the first variation is the one we want to use
                            variation_amount = variations[0].get('variation_amount')
                            if variation_amount:
                                # Update the amount field with the variation_amount
                                amount = Decimal(variation_amount)
                                print(f"Updated Amount from API: {amount}")
                            else:
                                return Response({"error": "Variation amount not found in the response."}, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response({"error": "No variations found in the response."}, status=status.HTTP_400_BAD_REQUEST)

                        # Return a successful response with the updated amount
                        return Response({
                            "valid": True,
                            "message": "Validation successful.",
                            "content": content,
                            "amount": str(amount)  # Send the amount back to the frontend
                        }, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({
                    "valid": False,
                    "message": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        else:
            print("Serializer Errors:", serializer.errors)
            return Response({"error": "Invalid data provided.", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        

class JambRegistrationViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serviceID = request.data.get('serviceID')
        exam_type = request.data.get('exam_type')  # Corrected from 'ExamType' to match input field
        jamb_profile_id = request.data.get('jamb_profile_id')
        phone_number = request.data.get('phone_number')
        amount = request.data.get('amount')
        billers_code = request.data.get('billersCode')  

        print(f"Received data: {request.data}")

        data = request.data.dict()  # Convert QueryDict to regular dict
        serializer = JambRegistrationSerializer(data=data, context={'request': request})

        service_name = serviceID
        jamb_profile_id = int(request.data.get('billersCode', 0))

        verify_profile = {
            'billersCode': billers_code,
            "serviceID": serviceID,
            "type": "utme-mock",
        }

        # if not serializer.is_valid():
        #     print("Serializer Errors:", serializer.errors)
        #     return Response({"error": "Invalid data.", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
        if serializer.is_valid():

            jamb_profile_id_str = request.data.get('jamb_profile_id')

            if jamb_profile_id_str is not None:
                try:
                    jamb_profile_id = int(jamb_profile_id_str)
                except ValueError:
                    return Response({'error': 'Invalid jamb_profile_id. It must be an integer.'}, status=400)
            else:
                return Response({'error': 'jamb_profile_id is required.'}, status=400)
            try:
                with db_transaction.atomic():
                    # Validation checks
                    if jamb_profile_id is None:
                        return Response({"error": "Jamb profile id and amount are required."}, status=status.HTTP_400_BAD_REQUEST)

                    if phone_number is None:
                        return Response({"error": "Phone number is required."}, status=status.HTTP_400_BAD_REQUEST)

                    # Validate that amount is a positive value
                    try:
                        amount = Decimal(str(amount))
                        if amount <= 0:
                            raise ValidationError("Amount must be a positive value.")
                    except ValueError:
                        return Response({"error": "Amount must be a valid number."}, status=status.HTTP_400_BAD_REQUEST)

                    # Check if the user has enough balance
                    user_balance = request.user.balance
                    total_amount = Decimal(amount)
                    if user_balance < total_amount:
                        return Response({"error": "Insufficient balance to complete this transaction."}, status=status.HTTP_400_BAD_REQUEST)

                    # Create the JambRegistration instance
                    jamb_registration = serializer.save(user=request.user)

                    # Process the transaction
                    transaction = Transaction.objects.create(
                        user=request.user,
                        transaction_type='Jamb Pin Generation',
                        amount=total_amount,
                        status='pending',  # Pending status initially
                        description=f"Payment for {jamb_profile_id} Jamb pins generation.",
                        product_name=jamb_registration.exam_type,
                        unique_element=jamb_registration.phone_number,
                        transaction_id=None
                    )

                    # Deduct balance from the user's account
                    request.user = jamb_registration.process_purchase()
                    request.user.save()

                    print(f"Jamb Profile Id : {jamb_profile_id}")

                    remaining_balance = request.user.balance
                    print(f"Balance after deduction: {remaining_balance}")
                
                    date_time_format = Mdate.now().strftime("%Y%m%d%H%M%S")
                    data = {
                        'request_id': str(date_time_format) + create_random_id(),
                        "serviceID": serviceID,
                        "variation_code": "utme-mock",
                        "billersCode": jamb_profile_id,
                        "phone": phone_number
                    }
                    print(data)

                    # Call he Jamb_Vending_Pin API
                    api = VTPassEducationAPI(
                        base_url="https://sandbox.vtpass.com",
                        auth_token = settings.VTPASS_AUTH_TOKEN,
                        secret_key = settings.VTPASS_SECRET_KEY  # Replace with your actual secret key
                    )
                    Jamb_Vending_Pin = api.Jamb_Vending_Pin(data)

                    transaction.transaction_id = Jamb_Vending_Pin.get("requestId", 'N/A')

                    # Regardless of transaction success, create the TVService instance
                    Jamb_Pin_Generator = JambRegistration.objects.create(
                        user=request.user,
                        serviceID=serviceID,
                        exam_type=exam_type,
                        jamb_profile_id=jamb_profile_id,
                        amount=Decimal(str(amount)),
                        phone_number=phone_number,
                        data_response=Jamb_Vending_Pin,  # Save the response
                        transaction_id=None,
                    )

                    Jamb_Pin_Generator.transaction_id = Jamb_Vending_Pin.get("requestId", 'N/A')
                    Jamb_Pin_Generator.save()  # Don't forget to save it

                    # Serialize the jamb_registration instance
                    serialized_jamb_registration = JambRegistrationSerializer(jamb_registration).data

                    # Get the user from the request (Django's authenticated user)
                    user = request.user

                    transaction_status = Jamb_Vending_Pin.get("content", {}).get("transactions", {}).get("status")
                    print(f"API Response Status: {transaction_status}")

                    if transaction_status == "delivered":
                        commission = Jamb_Vending_Pin.get("content", {}).get("transactions", {}).get("commission", 0)
                        commission = Decimal(commission)
                        user.bonus += commission
                        user.save()

                        transaction.status = 'completed'
                        transaction.save()
                        print(f"Transaction status updated to: {transaction.status}")


                        # Return success response with remaining balance and other details
                        return Response({
                            'success': True,
                            'message': f'{jamb_profile_id} JAMB pin(s) generated successfully.',
                            'remaining_balance': str(remaining_balance),
                            'transaction_id': transaction.transaction_id,
                            'data': serialized_jamb_registration,
                            "content": Jamb_Vending_Pin
                        }, status=status.HTTP_201_CREATED)

                    else:
                        # If the API fails, log the failure and revert the balance
                        print(f"API failed, reverting balance. Original user balance: {remaining_balance}, Deducted amount: {total_amount}")

                        # Revert the deducted balance
                        refund_amount = Jamb_Vending_Pin.get('amount', '0.00')
                        user.balance += total_amount
                        user.save()

                        # Mark the transaction as failed
                        transaction.status = 'failed'
                        transaction.save()

                        print(f"Balance after reversion: {user.balance}")

                        # Return error response due to API failure
                        return Response({
                            'success': False,
                            'error': 'Transaction failed with the external API.',
                            'details':Jamb_Vending_Pin,
                            'message': Jamb_Vending_Pin.get("response_description"),
                            'refund_amount': refund_amount,
                            'transaction_id': Jamb_Vending_Pin.get("requestId")
                        }, status=status.HTTP_400_BAD_REQUEST)

            except ValidationError as e:
                # Handle validation error
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

            except IntegrityError as e:
                print(f"Database integrity error: {str(e)}")
                return Response({"error": "Database integrity issue."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            except Exception as e:
                print(f"Unexpected error: {str(e)}")
                return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
     
        
        elif exam_type != '' and serviceID !='' and not phone_number and not amount and not jamb_profile_id:
            try:
                if exam_type is None and serviceID is not None:
                    return Response({"error": "Exam Type Field is required."}, status=status.HTTP_400_BAD_REQUEST)
                
                # Call the VTPass API to verify the exam type
                api = VTPassEducationAPI(
                    base_url="https://sandbox.vtpass.com",
                    auth_token = settings.VTPASS_AUTH_TOKEN,
                    secret_key = settings.VTPASS_SECRET_KEY # Replace with your actual secret key
                )
                get_variation_code = api.fetch_service_variations(service_name)

                # Check if the response is valid and parse it as JSON if needed
                if isinstance(get_variation_code, str):  # If the response is a string, parse it as JSON
                    get_variation_code = json.loads(get_variation_code)  # Assuming `json` is imported

                # Now we can safely access the 'content' field
                if get_variation_code:
                    content = get_variation_code.get('content', {})
                    if content.get('error'):
                        return Response({
                            "valid": False,
                            "message": content.get('error'),  # Show the error message from the content
                            "content": content
                        }, status=status.HTTP_200_OK)
                    else:
                        variations = content.get('variations', [])
                        if variations:
                            # Assume the first variation is the one we want to use
                            variation_amount = variations[0].get('variation_amount')
                            if variation_amount:
                                # Update the amount field with the variation_amount
                                amount = Decimal(variation_amount)
                                print(f"Updated Amount from API: {amount}")
                            else:
                                return Response({"error": "Variation amount not found in the response."}, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response({"error": "No variations found in the response."}, status=status.HTTP_400_BAD_REQUEST)

                        # Return a successful response with the updated amount
                        return Response({
                            "valid": True,
                            "message": "Validation successful.",
                            "content": content,
                            "amount": str(amount)  # Send the amount back to the frontend
                        }, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({
                    "valid": False,
                    "message": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        elif billers_code != '' and serviceID !='':   
            try:
                if billers_code is None and serviceID is not None:
                    return Response({"error": "JAMB ProfileID and Phone Number Field are required."}, status=status.HTTP_400_BAD_REQUEST)
                
                # Call the VTPass API to verify the exam type
                api = VTPassEducationAPI(
                    base_url="https://sandbox.vtpass.com",
                    auth_token = settings.VTPASS_AUTH_TOKEN,
                    secret_key = settings.VTPASS_SECRET_KEY  # Replace with your actual secret key
                )
                verify_jamb_profile = api.Verify_jamb_profile(verify_profile)

                # Check if the response is valid and parse it as JSON if needed
                if isinstance(verify_jamb_profile, str):  # If the response is a string, parse it as JSON
                    verify_jamb_profile = json.loads(verify_jamb_profile)  # Assuming `json` is imported

                # Now we can safely access the 'content' field
                if verify_jamb_profile:
                    content = verify_jamb_profile.get('content', {})
                    if content.get('error'):
                        return Response({
                            "valid": False,
                            "message": content.get('error'),  # Show the error message from the content
                            "content": content
                        }, status=status.HTTP_200_OK)
                    else:
                        # Return a successful response with the updated amount
                        return Response({
                            "valid": True,
                            "message": "Validation successful.",
                            "content": content,
                            "amount": str(amount)  # Send the amount back to the frontend
                        }, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({
                    "valid": False,
                    "message": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        else:
            print("Serializer Errors:", serializer.errors)
            return Response({"error": "Invalid data provided.", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            






















    

# class TransactionListView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         """
#         Return a list of all transactions for the authenticated user.
#         """
#         # Filter the transactions for the current user
#         transactions = Transaction.objects.filter(user=request.user).order_by('-timestamp')

#         # Serialize the data
#         serializer = TransactionSerializer(transactions, many=True)

#         return Response(serializer.data, status=status.HTTP_200_OK)


# class WalletBalanceView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         """Get the user's wallet balance."""
#         try:
#             wallet = request.user.wallet
#             serializer = WalletSerializer(wallet)
#             return Response(serializer.data)
#         except Wallet.DoesNotExist:
#             return Response({'detail': 'Wallet not found.'}, status=status.HTTP_404_NOT_FOUND)

# class DepositView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request):
#         """Deposit funds into the wallet."""
#         amount = request.data.get('amount')

#         if amount <= 0:
#             return Response({"detail": "Amount must be positive."}, status=status.HTTP_400_BAD_REQUEST)

#         wallet = request.user.wallet
#         wallet.deposit(amount)

#         # Record the transaction
#         transaction = Transaction.objects.create(
#             user=request.user,
#             wallet=wallet,
#             transaction_type='deposit',
#             amount=amount
#         )

#         return Response({'detail': f'Deposited {amount} to wallet.'}, status=status.HTTP_200_OK)

# class WithdrawView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request):
#         """Withdraw funds from the wallet."""
#         amount = request.data.get('amount')

#         if amount <= 0:
#             return Response({"detail": "Amount must be positive."}, status=status.HTTP_400_BAD_REQUEST)

#         wallet = request.user.wallet
#         try:
#             wallet.withdraw(amount)
#         except ValueError as e:
#             return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

#         # Record the transaction
#         transaction = Transaction.objects.create(
#             user=request.user,
#             wallet=wallet,
#             transaction_type='withdrawal',
#             amount=amount
#         )

#         return Response({'detail': f'Withdrew {amount} from wallet.'}, status=status.HTTP_200_OK)

# class TransferView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request):
#         """Transfer funds to another user's wallet."""
#         to_user_id = request.data.get('to_user_id')
#         amount = request.data.get('amount')

#         if amount <= 0:
#             return Response({"detail": "Amount must be positive."}, status=status.HTTP_400_BAD_REQUEST)

#         if to_user_id == request.user.id:
#             return Response({"detail": "You cannot transfer to yourself."}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             to_user = User.objects.get(id=to_user_id)
#             to_wallet = to_user.wallet
#         except User.DoesNotExist:
#             return Response({"detail": "Recipient user not found."}, status=status.HTTP_404_NOT_FOUND)

#         wallet = request.user.wallet
#         try:
#             wallet.transfer(to_wallet, amount)
#         except ValueError as e:
#             return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

#         # Create transaction records for both sender and recipient
#         Transaction.objects.create(
#             user=request.user,
#             wallet=wallet,
#             transaction_type='transfer',
#             amount=amount
#         )
#         Transaction.objects.create(
#             user=to_user,
#             wallet=to_wallet,
#             transaction_type='transfer',
#             amount=amount
#         )

#         return Response({'detail': f'Transferred {amount} to {to_user.username}.'}, status=status.HTTP_200_OK)