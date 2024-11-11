# import time
# from django.shortcuts import render, redirect, get_object_or_404
# from django.http import JsonResponse
# from rest_framework.exceptions import ValidationError

# from authentication.models import Profile
from api.serializer import RegisterSerializer, LoginSerializer

# from rest_framework.permissions import IsAuthenticated
# from rest_framework.authentication import TokenAuthentication

# from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from django.contrib.auth import authenticate, login

# from drf_yasg.utils import swagger_auto_schema

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

