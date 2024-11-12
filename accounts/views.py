from rest_framework import generics
from rest_framework.permissions import AllowAny

from accounts import serializers
from accounts.models import UserModel
from accounts.serializers import RegisterSerializers, LoginSerializer


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

class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    queryset = UserModel.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.validated_data['user']
        if not user.is_active:
            raise serializers.ValidationError("User is not active")
        return user