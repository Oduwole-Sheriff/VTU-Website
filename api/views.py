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

from api.serializer import RegisterSerializer, LoginSerializer, CustomUserSerializer, DepositSerializer, WithdrawSerializer, TransferSerializer, TransactionSerializer, AccountDetailsSerializer, BuyAirtimeSerializer, BuyDataSerializer
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from django.contrib.auth import authenticate, login
from Dashboard.models import CustomUser, Transaction, BuyData
from django.db import IntegrityError
from django.http import JsonResponse
from rest_framework.exceptions import ValidationError

from django.db import transaction as db_transaction

from RestAPI.AirtimeAPI import VTPassAPI
from RestAPI.DataAPI import VTPassDataAPI
import uuid
from datetime import datetime
import logging
import json
import random

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
                return Response({
                    'status': False,
                    'message': "Invalid password"
                }, status=status.HTTP_400_BAD_REQUEST)

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


    
class DepositView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = DepositSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            user = request.user  # Assuming the user is authenticated

            # Check if the amount is positive
            if amount <= 0:
                return Response({"detail": "Amount must be positive."}, status=status.HTTP_400_BAD_REQUEST)

            # Deposit funds to the user's balance
            user.deposit(amount)
            return Response(CustomUserSerializer(user).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

        # Serialize the data
        serializer = TransactionSerializer(transactions, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    

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
                    auth_token="Token be76014119dd44b12180ab93a92d63a2", 
                    secret_key="SK_873dc5215f9063f6539ec2249c8268bb788b3150386"
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
                    transaction_id = transactions.get('transactionId', '')
                    product_name = transactions.get('product_name', 'Unknown Product')

                    # Extract phone and unit price
                    phone_number = transactions.get('unique_element', 'None')
                    unit_price = transactions.get('unit_price', 0)

                    # Save the API response into airtime_response field
                    airtime_purchase.airtime_response = response  # Save the full response
                    airtime_purchase.save()

                    # Handle transaction status
                    if transaction_status == 'failed':
                        print(f"Transaction failed with transaction ID: {transaction_id}")
                        return self.handle_failed_transaction(transaction_id, response)

                    # If successful, save the transaction and return response
                    elif transaction_status == 'success':
                        # Deduct balance and save the successful transaction
                        request.user.balance -= float(amount)
                        request.user.save()

                        Transaction.objects.create(
                            user=request.user,
                            transaction_type='airtime_purchase',
                            amount=amount,
                            status='success',
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
        print(f"Transaction failed with transaction ID: {transaction_id}")
        print(f"API Response: {api_response}")

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
            transaction_type='airtime_purchase',
            amount=self.request.data.get('amount'),
            status='failed',
            product_name=product_name,
            transaction_id=transaction_id,  # Save the transaction ID
            unique_element=phone_number,  # Save the phone number from unique_element
            unit_price=unit_price,  # Save the unit price from the response
        )

        return Response({
            'status': 'failed',
            'message': message,
            'transaction_id': transaction_id,
            'response': api_response  # For debugging purposes
        }, status=status.HTTP_200_OK)




class BuyDataAPIView(APIView):
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
                        transaction_type='data_purchase',
                        amount=buy_data_instance.amount,
                        status='pending',  # Mark as pending initially
                        description=f"Data purchase for {buy_data_instance.data_plan}",
                        product_name=self.NETWORK_MAP.get(buy_data_instance.network, ""),  # Set the network as product_name
                        unit_price=buy_data_instance.amount,  # Set the unit_price to the amount
                        unique_element=buy_data_instance.mobile_number,
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
                    buy_data_instance.save()

                    if api_response and api_response.get("status") == "success":
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
                            'error': 'Transaction failed with the external API.',
                            'details': api_response
                        }, status=status.HTTP_400_BAD_REQUEST)

            except ValidationError as e:
                # Handle the exception and ensure balance reversion occurs
                print(f"Error during transaction: {e}")
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    def call_external_api(self, buy_data_instance, network, data_plan):
        """ Helper method to call the external API for purchasing data and fetching service variations. """
        base_url = "https://sandbox.vtpass.com"
        auth_token = "Token be76014119dd44b12180ab93a92d63a2"
        secret_key = "SK_873dc5215f9063f6539ec2249c8268bb788b3150386"
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