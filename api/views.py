# import time
# from django.shortcuts import render, redirect, get_object_or_404
# from django.http import JsonResponse
# from rest_framework.exceptions import ValidationError

# from authentication.models import Profile

# from rest_framework.permissions import IsAuthenticated
# from rest_framework.authentication import TokenAuthentication

# from django.contrib.auth import authenticate
# from drf_yasg.utils import swagger_auto_schema

from api.serializer import RegisterSerializer, LoginSerializer, WalletSerializer, TransactionSerializer
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from django.contrib.auth import authenticate, login
from Dashboard.models import Wallet, Transaction



from rest_framework import status, permissions



class RegisterAPI(APIView):

    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data = data)
        serializer.is_valid(raise_exception=True)

        if not serializer.is_valid():
            return Response({
                'status': False,
                'message': serializer.errors
            }, status.HTTP_400_BAD_REQUEST)

        serializer.save()
        
        return Response({'status': True, 'message': 'user created'}, status.HTTP_201_CREATED)


class LoginAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'message': serializer.errors
            }, status.HTTP_400_BAD_REQUEST)
        print(serializer.data)
        user = authenticate(request, username=serializer.data['username'], password=serializer.data['password'])
        if not user:
            return Response({
                'status': False,
                'message': "invalid credentials"
            }, status.HTTP_400_BAD_REQUEST)

        token, created = Token.objects.get_or_create(user=user)
        print(token)
        if user:
            login(request, user)
            return Response({'status': True, 'message': 'User logged in', 'token': token.key, 'redirect_url': '/'}, status=status.HTTP_200_OK)

        # token = Token.objects.get_or_create(user=user)
        # print(token)
        # return Response({'status': True, 'message': 'user login', 'token': str(token) }, status.HTTP_201_CREATED)

class WalletBalanceView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Get the user's wallet balance."""
        try:
            wallet = request.user.wallet
            serializer = WalletSerializer(wallet)
            return Response(serializer.data)
        except Wallet.DoesNotExist:
            return Response({'detail': 'Wallet not found.'}, status=status.HTTP_404_NOT_FOUND)

class DepositView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """Deposit funds into the wallet."""
        amount = request.data.get('amount')

        if amount <= 0:
            return Response({"detail": "Amount must be positive."}, status=status.HTTP_400_BAD_REQUEST)

        wallet = request.user.wallet
        wallet.deposit(amount)

        # Record the transaction
        transaction = Transaction.objects.create(
            user=request.user,
            wallet=wallet,
            transaction_type='deposit',
            amount=amount
        )

        return Response({'detail': f'Deposited {amount} to wallet.'}, status=status.HTTP_200_OK)

class WithdrawView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """Withdraw funds from the wallet."""
        amount = request.data.get('amount')

        if amount <= 0:
            return Response({"detail": "Amount must be positive."}, status=status.HTTP_400_BAD_REQUEST)

        wallet = request.user.wallet
        try:
            wallet.withdraw(amount)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Record the transaction
        transaction = Transaction.objects.create(
            user=request.user,
            wallet=wallet,
            transaction_type='withdrawal',
            amount=amount
        )

        return Response({'detail': f'Withdrew {amount} from wallet.'}, status=status.HTTP_200_OK)

class TransferView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """Transfer funds to another user's wallet."""
        to_user_id = request.data.get('to_user_id')
        amount = request.data.get('amount')

        if amount <= 0:
            return Response({"detail": "Amount must be positive."}, status=status.HTTP_400_BAD_REQUEST)

        if to_user_id == request.user.id:
            return Response({"detail": "You cannot transfer to yourself."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            to_user = User.objects.get(id=to_user_id)
            to_wallet = to_user.wallet
        except User.DoesNotExist:
            return Response({"detail": "Recipient user not found."}, status=status.HTTP_404_NOT_FOUND)

        wallet = request.user.wallet
        try:
            wallet.transfer(to_wallet, amount)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Create transaction records for both sender and recipient
        Transaction.objects.create(
            user=request.user,
            wallet=wallet,
            transaction_type='transfer',
            amount=amount
        )
        Transaction.objects.create(
            user=to_user,
            wallet=to_wallet,
            transaction_type='transfer',
            amount=amount
        )

        return Response({'detail': f'Transferred {amount} to {to_user.username}.'}, status=status.HTTP_200_OK)