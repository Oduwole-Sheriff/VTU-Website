# import time
# from django.shortcuts import render, redirect, get_object_or_404
# from django.http import JsonResponse
# from rest_framework.exceptions import ValidationError

# from authentication.models import Profile

from rest_framework.permissions import IsAuthenticated
# from rest_framework.authentication import TokenAuthentication

# from django.contrib.auth import authenticate
# from drf_yasg.utils import swagger_auto_schema

from api.serializer import RegisterSerializer, LoginSerializer, CustomUserSerializer, DepositSerializer, WithdrawSerializer, TransferSerializer, TransactionSerializer, AccountDetailsSerializer, BuyAirtimeSerializer
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from django.contrib.auth import authenticate, login
from Dashboard.models import CustomUser, Transaction
from django.db import IntegrityError
from django.http import JsonResponse
from rest_framework.exceptions import ValidationError

from RestAPI.AirtimeAPI import VTPassAPI
import uuid
from datetime import datetime
import logging
import json

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

                # Call the API and get the transaction response
                response = api.buy_airtime(api_data)

                # Debug: Print raw response from VTPass
                print(f"Raw response from VTPass: {response}")

                # If the response is a string (transaction ID), convert it to JSON
                if isinstance(response, str):
                    response = {
                        "status": "failed",  # Treat as failed transaction
                        "transactionId": response,
                        "product_name": "Unknown Product"  # Default product name if not provided
                    }
                    print(f"Converted string response to JSON: {response}")

                # Handle the response as JSON
                if isinstance(response, dict):
                    transaction_status = response.get('status', 'failed')
                    transaction_id = response.get('transactionId', '')
                    product_name = response.get('content', {}).get('transactions', {}).get('product_name', 'Unknown Product')

                    # Handle failed transaction
                    if transaction_status == 'failed':
                        print(f"Transaction failed with transaction ID: {transaction_id}")
                        return self.handle_failed_transaction(transaction_id, response)  # Pass the response here

                    # If the transaction is successful
                    elif transaction_status == 'success':
                        # Save the transaction as successful
                        Transaction.objects.create(
                            user=request.user,
                            transaction_type='airtime_purchase',
                            amount=amount,
                            status='success',  # Mark as successful
                            product_name=product_name,  # Use the product_name from the API response
                            unique_element=request.data.get('mobile_number'),
                            unit_price=amount,
                            description=f"Airtime purchase for {request.data.get('mobile_number')}",
                            transaction_id=transaction_id  # Save the transaction ID
                        )

                        # Debug: Print successful response
                        print(f"Transaction successful. Product Name: {product_name}, Transaction ID: {transaction_id}")

                        return Response({
                            'status': 'success',
                            'remaining_balance': str(remaining_balance),
                            'transaction_id': transaction_id,  # Include the transaction ID from VTPassAPI
                            'product_name': product_name  # Include the product name in the response
                        }, status=status.HTTP_200_OK)

                    else:
                        # Handle unexpected responses
                        print(f"Unexpected response from VTPass: {response}")
                        return Response({
                            'status': 'error',
                            'message': 'Transaction failed. Please check the details or try again.',
                            'response': response  # For debugging purposes
                        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                else:
                    # If response is not a string or dictionary, return error
                    print(f"Invalid response type from VTPass: {type(response)}. Response: {response}")
                    return Response({
                        'status': 'error',
                        'message': 'Invalid response from VTPass. Expected a JSON object or transaction ID.',
                        'response': response  # Include the raw response for debugging
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            except Exception as e:
                # Handle unexpected errors during the purchase process
                print(f"Unexpected error: {str(e)}")
                return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            # Print validation errors
            print(f"Validation errors: {serializer.errors}")
            # Return validation errors if data is invalid
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
        # Log the failure for debugging
        print(f"Transaction failed with transaction ID: {transaction_id}")
        print(f"API Response: {api_response}")  # Debug: Print the full API response

        # Extract the product name from the API response
        try:
            # Check if 'product_name' exists in the response and extract it correctly
            product_name = api_response.get('content', {}).get('transactions', {}).get('product_name', 'Unknown Product')

            if not product_name:
                # If no product_name, use a fallback
                print("Product name not found in the API response. Using fallback value.")
                product_name = 'Unknown Product'
            
        except KeyError as e:
            # Catch any key errors and log
            print(f"Error accessing product_name: {e}")
            product_name = 'Unknown Product'

        # Log the extracted product name
        print(f"Extracted Product Name: {product_name}")

        # Create and save the failed transaction in the database
        Transaction.objects.create(
            user=self.request.user,
            transaction_type='airtime_purchase',
            amount=self.request.data.get('amount'),
            status='failed',  # Explicitly set the status to 'failed'
            product_name=product_name,  # Use the extracted product name
            unique_element=self.request.data.get('mobile_number'),
            unit_price=self.request.data.get('amount'),
            description=f"Airtime purchase for {self.request.data.get('mobile_number')}",
            transaction_id=transaction_id  # Save the transaction ID
        )

        # Return the failure response
        return Response({
            'status': 'failed',
            'message': 'Transaction failed. Please check the details or try again.',
            'transaction_id': transaction_id,
            'product_name': product_name  # Include the product name in the response
        }, status=status.HTTP_200_OK)

















    

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