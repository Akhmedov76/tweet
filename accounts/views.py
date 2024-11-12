from http.client import responses
from msilib import Table

from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from setuptools.package_index import user_agent

from accounts import serializers
from accounts.models import UserModel
from accounts.serializers import RegisterSerializers, LoginSerializer, VerificationSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializers
    queryset = UserModel.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.is_active = False
        user.save()
        return user


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh = RefreshToken.for_user(user=serializer.validated_data['user'])

        response = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "message": "Logged in successfully",
        }

        return Response(response, status=status.HTTP_200_OK)


class VerifyView(APIView):
    permission_classes = [AllowAny]
    serializer_class = VerificationSerializer

    def post(self, request):
        serializer = VerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_code = serializer.validated_data['user_code']
        user = user_code.user

        user.is_active = True
        user.save()
        user_code.delete()
        response = {
            "message": "Email verified successfully",
            "success": True,
        }

        return Response(response, status=status.HTTP_200_OK)
